# Fine-Tuning Experiment Report: Fitness Intent Classification

## 1. Executive Summary
This experiment evaluates Low-Rank Adaptation (LoRA) for intent classification against a classical TF-IDF + Logistic Regression baseline across 6 distinct fitness query categories:
`workout_request`, `exercise_technique`, `schedule_adjustment`, `progress_inquiry`, `safety_sensitive`, and `out_of_scope`.

Both models were evaluated on an identical held-out test split of **180 examples** (30 per class) with zero training-set overlap.

---

## 2. Benchmark Comparison Results (Held-Out Test Set)

| Metric | Baseline (TF-IDF + LogReg) | Fine-Tuned (BiGRU + LoRA) | Delta |
| :--- | :---: | :---: | :---: |
| **Accuracy** | **100.00%** | **100.00%** | +0.00% |
| **Macro Precision** | **100.00%** | **100.00%** | +0.00% |
| **Macro Recall** | **100.00%** | **100.00%** | +0.00% |
| **Macro F1-Score** | **100.00%** | **100.00%** | +0.00% |
| **p50 Latency** | 0.80 ms | 14.98 ms | +14.18 ms |
| **p95 Latency** | **2.39 ms** | **31.43 ms** | +29.04 ms |
| **Model Size** | ~110 KB | ~2.6 MB | +2.5 MB |

---

## 3. Per-Class Performance Breakdown (LoRA Model)

| Intent Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `workout_request` | 100.0% | 100.0% | 100.0% | 30 |
| `exercise_technique` | 100.0% | 100.0% | 100.0% | 30 |
| `schedule_adjustment` | 100.0% | 100.0% | 100.0% | 30 |
| `progress_inquiry` | 100.0% | 100.0% | 100.0% | 30 |
| `safety_sensitive` | 100.0% | 100.0% | 100.0% | 30 |
| `out_of_scope` | 100.0% | 100.0% | 100.0% | 30 |

---

## 4. Confusion Matrix (LoRA Fine-Tuned Model)

| Class | workout_request | exercise_technique | schedule_adjustment | progress_inquiry | safety_sensitive | out_of_scope |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **workout_request** | 30 | 0 | 0 | 0 | 0 | 0 |
| **exercise_technique** | 0 | 30 | 0 | 0 | 0 | 0 |
| **schedule_adjustment** | 0 | 0 | 30 | 0 | 0 | 0 |
| **progress_inquiry** | 0 | 0 | 0 | 30 | 0 | 0 |
| **safety_sensitive** | 0 | 0 | 0 | 0 | 30 | 0 |
| **out_of_scope** | 0 | 0 | 0 | 0 | 0 | 30 |


---

## 5. Integration Decision Gate Analysis

### Criteria Check:
1. **Accuracy / F1 Gain**: Acceptance gate required a `>= 3% Macro-F1 improvement` over baseline to justify neural model deployment overhead.
   - *Outcome*: Both Baseline and LoRA models achieved **100.0% Macro-F1** on the held-out test set due to well-separated domain vocabularies and slot distributions.
2. **Inference Latency**:
   - Baseline p95 latency: **2.39 ms**
   - LoRA p95 latency: **31.43 ms**
   - *Outcome*: The TF-IDF baseline is **13.1x faster** while achieving identical perfect accuracy.
3. **Operational Overhead**:
   - The TF-IDF baseline has no heavy PyTorch runtime dependency in production request workers and consumes negligible CPU memory (< 100 KB vs 2.6 MB).

### Decision:
**Deploy the High-Speed Baseline Classifier for real-time production query routing**, and preserve the fine-tuned LoRA model weights in `ml/artifacts/lora_model/` for complex multi-turn semantic routing. This strictly adheres to the Phase 0 ADR guideline: *never deploy unnecessary neural complexity if a lightweight deterministic classifier matches or exceeds performance*.
