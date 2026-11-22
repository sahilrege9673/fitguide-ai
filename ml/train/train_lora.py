import json
import os
import math
import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Tuple
from peft import LoraConfig, TaskType

CLASSES = [
    "workout_request",
    "exercise_technique",
    "schedule_adjustment",
    "progress_inquiry",
    "safety_sensitive",
    "out_of_scope"
]
LABEL_TO_ID = {c: i for i, c in enumerate(CLASSES)}
ID_TO_LABEL = {i: c for i, c in enumerate(CLASSES)}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts", "lora_model")

class Vocabulary:
    def __init__(self, max_size: int = 5000):
        self.max_size = max_size
        self.word2idx = {"<PAD>": 0, "<UNK>": 1}
        self.idx2word = {0: "<PAD>", 1: "<UNK>"}

    def fit(self, texts: List[str]):
        freqs: Dict[str, int] = {}
        for text in texts:
            words = text.lower().replace("?", " ? ").replace(".", " . ").split()
            for w in words:
                freqs[w] = freqs.get(w, 0) + 1
        sorted_words = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
        for w, _ in sorted_words[:self.max_size - 2]:
            idx = len(self.word2idx)
            self.word2idx[w] = idx
            self.idx2word[idx] = w

    def encode(self, text: str, max_len: int = 64) -> List[int]:
        words = text.lower().replace("?", " ? ").replace(".", " . ").split()
        ids = [self.word2idx.get(w, 1) for w in words][:max_len]
        if len(ids) < max_len:
            ids += [0] * (max_len - len(ids))
        return ids

class IntentDataset(Dataset):
    def __init__(self, filepath: str, vocab: Vocabulary, max_len: int = 64):
        self.examples = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                input_ids = vocab.encode(row["text"], max_len=max_len)
                label_id = LABEL_TO_ID[row["label"]]
                self.examples.append((torch.tensor(input_ids, dtype=torch.long), torch.tensor(label_id, dtype=torch.long)))

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]

class LoRALinear(nn.Module):
    """
    Low-Rank Adaptation (LoRA) Linear Layer.
    W_new = W_base + (alpha / r) * (B @ A)
    Frozen base weight + trainable low-rank decomposition matrices.
    """
    def __init__(self, in_features: int, out_features: int, rank: int = 16, alpha: float = 32.0):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.scaling = alpha / rank

        # Frozen base weight
        self.base_linear = nn.Linear(in_features, out_features)
        self.base_linear.weight.requires_grad = False
        if self.base_linear.bias is not None:
            self.base_linear.bias.requires_grad = False

        # Trainable low-rank decomposition
        self.lora_A = nn.Parameter(torch.zeros(rank, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, rank))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))
        nn.init.zeros_(self.lora_B)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base_out = self.base_linear(x)
        lora_out = (x @ self.lora_A.T @ self.lora_B.T) * self.scaling
        return base_out + lora_out

class LoRASequenceClassifier(nn.Module):
    """
    Transformer-aligned neural classifier augmented with LoRA projection adapters.
    """
    def __init__(self, vocab_size: int, embed_dim: int = 128, hidden_dim: int = 256, num_classes: int = 6, rank: int = 16):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.encoder = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        # Low-rank adapted classification head
        self.classifier = LoRALinear(hidden_dim * 2, num_classes, rank=rank, alpha=32.0)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        embeds = self.embedding(input_ids)
        _, hidden = self.encoder(embeds)
        # Concatenate forward and backward final hidden states
        h_pool = torch.cat([hidden[-2], hidden[-1]], dim=-1)
        logits = self.classifier(h_pool)
        return logits

def train_lora_model(epochs: int = 8, batch_size: int = 32, lr: float = 2e-3, rank: int = 16):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using compute device: {device}")

    # 1. Load data
    train_file = os.path.join(DATA_DIR, "train.jsonl")
    val_file = os.path.join(DATA_DIR, "val.jsonl")

    train_texts = [json.loads(line)["text"] for line in open(train_file, encoding="utf-8")]
    vocab = Vocabulary(max_size=4000)
    vocab.fit(train_texts)

    train_ds = IntentDataset(train_file, vocab)
    val_ds = IntentDataset(val_file, vocab)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # 2. Instantiate LoRA Model
    model = LoRASequenceClassifier(
        vocab_size=len(vocab.word2idx),
        embed_dim=128,
        hidden_dim=256,
        num_classes=len(CLASSES),
        rank=rank
    ).to(device)

    # Count trainable vs frozen parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen_params = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    print(f"\n--- LoRA Parameter Summary ---")
    print(f"Total Parameters:     {trainable_params + frozen_params:,}")
    print(f"Trainable Parameters: {trainable_params:,} ({(trainable_params / (trainable_params + frozen_params)) * 100:.2f}%)")
    print(f"Frozen Base Weights:  {frozen_params:,}")

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr, weight_decay=1e-4)

    # 3. Training Loop
    print("\nStarting LoRA Fine-Tuning...")
    start_time = time.time()
    best_val_acc = 0.0

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        correct, total = 0, 0

        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(batch_y)
            preds = torch.argmax(logits, dim=-1)
            correct += (preds == batch_y).sum().item()
            total += len(batch_y)

        train_acc = correct / total
        avg_loss = total_loss / total

        # Validation Step
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                logits = model(batch_x)
                preds = torch.argmax(logits, dim=-1)
                val_correct += (preds == batch_y).sum().item()
                val_total += len(batch_y)

        val_acc = val_correct / val_total
        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {avg_loss:.4f} | Train Acc: {train_acc*100:.1f}% | Val Acc: {val_acc*100:.1f}%")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            # Save best checkpoint
            torch.save(model.state_dict(), os.path.join(ARTIFACTS_DIR, "best_lora_weights.pt"))

    train_time = time.time() - start_time
    print(f"\nTraining completed in {train_time:.2f} seconds. Best Val Accuracy: {best_val_acc*100:.2f}%")

    # Save metadata & vocab
    config_dict = {
        "classes": CLASSES,
        "vocab_size": len(vocab.word2idx),
        "rank": rank,
        "alpha": 32.0,
        "embed_dim": 128,
        "hidden_dim": 256,
        "best_val_acc": round(best_val_acc, 4),
        "training_time_secs": round(train_time, 2)
    }
    with open(os.path.join(ARTIFACTS_DIR, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)

    with open(os.path.join(ARTIFACTS_DIR, "vocab.json"), "w", encoding="utf-8") as f:
        json.dump(vocab.word2idx, f, indent=2)

    print(f"Model artifacts and LoRA configuration saved to {ARTIFACTS_DIR}")

if __name__ == "__main__":
    train_lora_model()
