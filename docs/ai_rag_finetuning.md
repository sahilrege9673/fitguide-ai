# Section 6: AI Architecture, RAG Pipeline & Fine-Tuning Specification

## 1. AI System Overview & Service Abstraction

FeedGuide AI integrates artificial intelligence through a decoupled, multi-layered architecture:

```
┌────────────────────────────────────────────────────────┐
│                   Inbound User Prompt                  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
              ┌───────────────────────────┐
              │  1. Safety Engine Check   │ ──(Violates)──► [Immediate Refusal / Doctor Notice]
              └─────────────┬─────────────┘
                            │ (Passes)
                            ▼
              ┌───────────────────────────┐
              │ 2. Intent Classification  │ (Fine-Tuned LoRA / Baseline Router)
              └─────────────┬─────────────┘
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
      [Workout / General]        [Knowledge / Science]
               │                         │
               │                         ▼
               │              ┌───────────────────────────┐
               │              │ 3. pgvector RAG Retrieval │
               │              └──────────┬────────────────┘
               │                         │ (Top-k Chunks)
               ▼                         ▼
        ┌──────────────────────────────────────┐
        │    4. User Context Assembler         │
        │    (Profile + Schedule + Logs)       │
        └──────────────────┬───────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │   5. Provider-Agnostic LLM Engine    │
        │    (Gemini 1.5 Flash / Fallback)     │
        └──────────────────┬───────────────────┘
                           │
                           ▼
        ┌──────────────────────────────────────┐
        │  6. Structured Pydantic Repair /     │
        │     Streaming SSE Token Emitter      │
        └──────────────────────────────────────┘
```

---

## 2. Token-Efficient Context Builder

To prevent token bloat, reduce latency, and maximize grounding quality, the context builder compiles a compact state summary per user query:

```python
# apps/api/app/services/context_builder.py

from typing import Dict, Any

class UserContextBuilder:
    @staticmethod
    def build_compact_context(
        profile: Dict[str, Any],
        preferences: Dict[str, Any],
        this_week_schedule: list,
        recent_sessions: list
    ) -> str:
        """
        Compresses live user state into an ultra-compact ~150-250 token Markdown snippet.
        """
        age_group = preferences.get("age_group", "adult_18_64")
        experience = preferences.get("experience_level", "intermediate")
        goals = ", ".join(preferences.get("fitness_goals", []))
        equipment = ", ".join(preferences.get("available_equipment", []))
        location = preferences.get("workout_location", "gym")
        time_avail = preferences.get("time_availability_mins", 45)

        # Recent completed volume & fatigue summary
        recent_summary = []
        for s in recent_sessions[:3]:
            recent_summary.append(f"- {s['title']} ({s['focus_area']}): RPE {s.get('perceived_exertion', 'N/A')}")
        recent_text = "\n".join(recent_summary) if recent_summary else "No recent workouts logged."

        # Active weekly schedule status
        sched_days = [f"{entry['scheduled_date']}: {entry['title']} ({'DONE' if entry['is_completed'] else 'PENDING'})" for entry in this_week_schedule]
        sched_text = "; ".join(sched_days) if sched_days else "Schedule uninitialized."

        return f"""
### ATHLETE SNAPSHOT (UNTRUSTED DATA)
- Demographic: {age_group} | Level: {experience} | Time: {time_avail} mins/session
- Goals: {goals} | Location: {location}
- Available Equipment: {equipment}
- Recent Workouts:
{recent_text}
- This Week's Plan: {sched_text}
""".strip()
```

---

## 3. Structured Outputs & Pydantic Validation

When generating workouts or exercise swaps, the LLM must return strict JSON matching Pydantic schemas. Every exercise ID in the output must exist in the database catalog:

```python
# apps/api/app/schemas/workout_llm.py

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional

class LLMExerciseRecommendation(BaseModel):
    exercise_id: UUID4 = Field(..., description="Exact UUID from exercises database")
    exercise_name: str
    target_sets: int = Field(..., ge=1, le=8)
    target_reps: Optional[int] = Field(None, ge=1, le=50)
    target_duration_secs: Optional[int] = Field(None, ge=10, le=1800)
    target_rest_secs: int = Field(60, ge=15, le=300)
    coaching_cue: str = Field(..., max_length=150)

class LLMWorkoutPlanResponse(BaseModel):
    session_title: str
    focus_area: str
    estimated_duration_mins: int
    rationale: str
    exercises: List[LLMExerciseRecommendation]
```

### Automatic Repair Strategy:
1. If the LLM generates an unknown `exercise_id`, the backend automatically resolves it via fuzzy match on `exercise_name` against the active catalog.
2. If resolution fails, the invalid exercise is swapped with the closest category/muscle match from the database.
3. If JSON syntax is invalid, a single retry prompt is fired with the JSON error trace (`temperature=0.0`).

---

## 4. RAG Pipeline Specification (Phase 4)

### 4.1 Curated Knowledge Corpus
The RAG pipeline ingests peer-reviewed, authoritative public health and athletic training guidelines:
- American College of Sports Medicine (ACSM) Guidelines for Exercise Testing and Prescription.
- World Health Organization (WHO) Guidelines on Physical Activity and Sedentary Behaviour.
- National Strength and Conditioning Association (NSCA) Foundations of Fitness & Youth Resistance Training Position Statements.
- National Institute on Aging (NIA) Exercise & Physical Activity Guidelines.

All ingested documents track license, attribution, and original publication URLs.

### 4.2 Ingestion & Chunking Specification
- **Parsing**: Clean Markdown and PDF loaders stripped of headers, footers, and table-of-contents noise.
- **Chunk Size**: Target **350–450 tokens** with **50-token sliding overlap** using `RecursiveCharacterTextSplitter`.
- **Metadata Tagging**: Every chunk receives:
  ```json
  {
    "document_title": "ACSM Position Stand on Youth Resistance Training",
    "source_url": "https://www.acsm.org/...",
    "category": "youth_training",
    "target_age_groups": ["minor_under_18"],
    "chunk_index": 14
  }
  ```

### 4.3 Vector Embeddings & pgvector HNSW Index
- **Model**: Google `text-embedding-004` (768 dimensions).
- **Index Configuration**:
  ```sql
  CREATE INDEX idx_knowledge_chunks_embedding_hnsw 
  ON knowledge_chunks 
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
  ```
- **Retrieval Logic**:
  Cosine similarity search filtering by `metadata->>'target_age_groups'` matching the user's age category:
  ```sql
  SELECT id, document_id, content, metadata, 
         1 - (embedding <=> $query_embedding) AS similarity_score
  FROM knowledge_chunks
  WHERE (metadata->'target_age_groups' ? $user_age_group OR metadata->'target_age_groups' IS NULL)
  ORDER BY embedding <=> $query_embedding ASC
  LIMIT 4;
  ```

### 4.4 Weak-Retrieval Fallback & Grounded Citations
- If maximum `similarity_score` < 0.68, the system does not hallucinate. It executes the fallback:
  > *"I don't have enough verified evidence in my fitness knowledge base to give a definitive answer to this specific question. Here is what is generally recommended for your profile..."*
- When evidence is strong (score >= 0.68), citations are appended inline: `[Source: ACSM Guidelines, 2023]`.

### 4.5 Retrieval Evaluation Harness
A benchmark suite of 30 curated question-source pairs will evaluate Top-1 and Top-3 retrieval hit rate (target >= 85% Top-3).

---

## 5. Fine-Tuning Experiment Specification (Phase 5)

### 5.1 Experiment Goal: Fitness-Intent Classification
Rather than risking hallucinations by fine-tuning a small generative model on medical advice, fine-tuning is dedicated to **Intelligent Query Intent Routing**. This routes incoming user prompts into 6 deterministic buckets:
1. `workout_request`: "Give me a shoulder workout for dumbbells only."
2. `exercise_technique`: "How do I keep my knees from caving during lunges?"
3. `schedule_adjustment`: "I need to move tomorrow's session to Friday."
4. `progress_inquiry`: "How much has my squat volume increased this month?"
5. `safety_sensitive`: "My lower back is throbbing after deadlifts."
6. `out_of_scope`: "What is the capital of France?"

### 5.2 Curated Dataset Specification
- **Size**: 1,200 labeled examples (200 per class).
- **Split**: 70% Train (840), 15% Validation (180), 15% Test (180).
- **Zero Leakage**: Strict split by unique user utterance clusters to prevent memorization.

### 5.3 Training Configuration (LoRA / PEFT)
- **Base Model**: `distilbert-base-uncased` or `google/gemma-2-2b-it` (runnable on free Google Colab T4 GPU or local machine).
- **PEFT Method**: LoRA (Low-Rank Adaptation)
  - `r = 16`, `lora_alpha = 32`, `lora_dropout = 0.05`
  - Target modules: `q_proj`, `v_proj` (or equivalent query/value attention heads)
  - Learning rate: `2e-4`, Batch size: 16, Epochs: 4
  - Optimizer: AdamW with cosine learning rate schedule.

### 5.4 Evaluation & Integration Criteria
- **Metrics**: Accuracy, Per-Class Precision, Recall, Macro-F1, and Confusion Matrix.
- **Baseline**: Zero-shot prompt with `gemini-1.5-flash` or a lightweight TF-IDF + LogisticRegression baseline.
- **Integration Rule**: The fine-tuned LoRA model is integrated into the production FastAPI pipeline *only* if its Macro-F1 exceeds the baseline by >= 3% with lower p95 latency (< 50ms). Otherwise, the results and rationale are fully documented in `ml/reports/finetuning_report.md` without polluting production. Real metrics only; zero fabrication.
