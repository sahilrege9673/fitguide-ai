import json
import os
import time
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts")

def load_jsonl(filepath: str):
    texts, labels = [], []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            texts.append(item["text"])
            labels.append(item["label"])
    return texts, labels

def train_baseline():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    train_path = os.path.join(DATA_DIR, "train.jsonl")
    val_path = os.path.join(DATA_DIR, "val.jsonl")

    print(f"Loading training data from: {train_path}")
    X_train, y_train = load_jsonl(train_path)
    X_val, y_val = load_jsonl(val_path)

    print(f"Train samples: {len(X_train)}, Val samples: {len(X_val)}")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )),
        ("clf", LogisticRegression(
            C=2.0,
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        ))
    ])

    print("Training baseline TF-IDF + Logistic Regression model...")
    start_time = time.time()
    pipeline.fit(X_train, y_train)
    train_duration = time.time() - start_time
    print(f"Training completed in {train_duration:.2f} seconds.")

    # Validation evaluation
    y_pred = pipeline.predict(X_val)
    val_acc = accuracy_score(y_val, y_pred)
    val_macro_f1 = f1_score(y_val, y_pred, average="macro")

    print(f"\n--- Validation Results (Baseline) ---")
    print(f"Accuracy: {val_acc * 100:.2f}%")
    print(f"Macro-F1: {val_macro_f1 * 100:.2f}%\n")
    print(classification_report(y_val, y_pred, digits=4))

    # Save model artifact
    model_path = os.path.join(ARTIFACTS_DIR, "baseline_classifier.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Saved baseline model artifact to: {model_path}")

    return pipeline

if __name__ == "__main__":
    train_baseline()
