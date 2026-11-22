# Section 8: Implementation Plan & Phase Exit Criteria

## 1. Operating Rules & Verification Gate Protocol

FitGuide AI is constructed in **strictly sequential phases** (Phases 0 through 7).
Advancing to a subsequent phase is prohibited until all exit criteria for the current phase are verified and explicit user approval is granted.

### Strict Non-Regression Invariants:
1. **Never Advance With Broken Features**: Broken authentication, database errors, or regressions in earlier phases halt progression immediately.
2. **Four-State Coverage**: Every screen delivered must implement Loading (skeleton), Empty, Error, and Success states.
3. **No Fabricated Data or Responses**: Real database operations and verified API integrations only.
4. **Design Compliance**: Adherence to the 6 palette tokens, Space Grotesk/Inter typography, sharp geometry (max 6px radius), and authentic imagery.

---

## 2. Phase-by-Phase Roadmap

### Phase 0 — Planning & Architecture (CURRENT)
- **Deliverables**: Comprehensive architecture artifacts in `/docs`:
  - Requirements analysis & stack rationale.
  - Monorepo directory map.
  - Sitemap, navigation tree, and 4-state UX definitions.
  - ERD, full PostgreSQL schema, and RLS policy plan.
  - Complete `/api/v1/...` REST contract specifications (`/docs/api.md`).
  - Clinical safety rules and age-appropriate invariant specification (`/docs/safety_rules.md`).
  - AI context builder, structured output schemas, RAG and Fine-tuning plan (`/docs/ai_rag_finetuning.md`).
  - Design system tokens, typography, motion rules, and imagery guidelines (`/docs/design_system.md`).
  - Credentials and environment configuration checklist (`/docs/credentials_and_env.md`).
- **Exit Criteria**:
  - All Phase 0 architectural documents delivered and validated.
  - Zero application code written before formal sign-off.
  - Post Phase 0 report and await explicit approval.

---

### Phase 1 — Foundation & Authentication
- **Deliverables**:
  - Scaffold `apps/web` (Next.js 14 App Router, TypeScript strict, Tailwind with custom tokens).
  - Scaffold `apps/api` (FastAPI with CORS, Pydantic settings, health endpoint).
  - Supabase database configuration and initial migration scripts (`001_initial_schema.sql`, `002_enable_pgvector.sql`, `003_rls_policies.sql`, `004_indexes.sql`).
  - Supabase Auth integration (Email/Password registration, login, Google OAuth, email verification, password recovery).
  - FastAPI Supabase JWT authentication middleware (deriving `user_id` strictly from token `sub` claim).
  - Public marketing landing page matching athletic design system.
  - Login, registration, and multi-step onboarding wizard with persistent auto-save to `onboarding_preferences`.
  - Mandatory fitness disclaimer acceptance gate.
  - Automated RLS test suite verifying cross-user isolation.
- **Exit Criteria**:
  - A new user can register, verify email, complete onboarding, and land on a protected route.
  - RLS test suite passes: User B cannot read or mutate User A's profile or preferences.
  - Backend returns 401 Unauthorized for missing or invalid JWTs.
  - Phase 1 report posted and user approval received.

---

### Phase 2 — Core Application
- **Deliverables**:
  - Dashboard hub with daily greeting, today's prescribed workout card, upcoming schedule list, and completion ring.
  - Exercise Library (`/exercises`) with search, multi-filter (muscle, category, difficulty, equipment), and detail view (`/exercises/[slug]`) featuring cited media.
  - Database seed script inserting >= 80 verified exercises with accurate biomechanical instructions and attribution.
  - Deterministic rule-based workout plan generator aware of user age group, available equipment, time budget, and goals.
  - Daily workout execution player (`/workouts/[id]`): exercise instructions, target sets/reps, active timer, set logging (`exercise_logs`).
  - Post-workout completion flow and feedback capture (`feedback` table).
  - Weekly schedule and calendar view (`/schedule`) with rest day visualization and rescheduling.
  - User profile and settings screen (`/profile`) with preference updates.
- **Exit Criteria**:
  - User completes end-to-end journey: Onboarding -> Generates Plan -> Executes & Logs Workout -> Workout appears in history, schedule, and dashboard.
  - All screens implement Loading, Empty, Error, and Success states.
  - Phase 2 report posted and user approval received.

---

### Phase 3 — AI Integration & Grounded Chat
- **Deliverables**:
  - Provider-agnostic LLM service layer (`LLMProvider`) supporting Google Gemini API with fallback adapter.
  - Real-time streaming AI Assistant chat (`/assistant`) with persistent conversations and messages in Supabase.
  - Compact user context assembler injecting profile, goals, weekly schedule, and recent workout fatigue.
  - Deterministic safety pre-check and post-check (`safety_rules.py`) intercepting red flags and age-inappropriate requests.
  - Pydantic structured output validation and automatic repair for AI workout modifications.
  - Per-user rate limiting on chat endpoints (15 req/min).
- **Exit Criteria**:
  - Chatbot demonstrably grounds answers in the authenticated user's actual profile and workout history.
  - Red flags (chest pain, injury, extreme deficits) trigger immediate refusal and clinical advisory.
  - Chat streaming functions without token buffering or UI freezing.
  - Phase 3 report posted and user approval received.

---

### Phase 4 — RAG Pipeline
- **Deliverables**:
  - Curated exercise science and public health reference documents ingested into `knowledge_documents`.
  - Ingestion and chunking script (`300-500 tokens` with overlap) generating 768-dimensional embeddings.
  - pgvector HNSW index setup and cosine similarity retrieval service with age-group metadata filtering.
  - Inline source citations appended to grounded AI responses (`[Source: ACSM Guidelines]`).
  - Weak-retrieval fallback mechanism answering "I don't have enough verified information" when similarity is below threshold.
  - Automated retrieval benchmark test suite evaluating Top-1 and Top-3 hit rate.
- **Exit Criteria**:
  - AI responses to exercise science questions include verified inline citations.
  - Weak queries trigger transparent fallbacks rather than hallucinations.
  - Retrieval hit rate benchmark yields >= 85% Top-3 accuracy on the test set.
  - Phase 4 report posted and user approval received.

---

### Phase 5 — Fine-Tuning Experiment
- **Deliverables**:
  - Clear task definition: 6-class Fitness-Intent Classification.
  - Curated, leak-free dataset in `ml/data/` (train, val, test splits).
  - Reproducible LoRA/PEFT training script for Hugging Face Transformers (`ml/train/train_lora.py`).
  - Evaluation harness (`ml/eval/evaluate_model.py`) reporting Accuracy, Per-Class Precision, Recall, Macro-F1, and Confusion Matrix.
  - Baseline comparison against zero-shot LLM.
  - Documented write-up (`ml/reports/finetuning_report.md`) detailing training loss curves, compute requirements, honest metrics, and integration decision.
- **Exit Criteria**:
  - Reproducible training and evaluation scripts run successfully without errors.
  - Honest, non-fabricated metrics published.
  - Clear decision documented whether to deploy or retain baseline router.
  - Phase 5 report posted and user approval received.

---

### Phase 6 — Analytics, Reports & Advanced Features
- **Deliverables**:
  - Restrained athletic analytics dashboard (`/progress`): weekly volume trends, consistency score, muscle group distribution.
  - AI-generated weekly retrospective summary grounded in logged exercise data.
  - Post-workout feedback loop dynamically adjusting future plan intensity based on soreness and difficulty ratings.
  - Dynamic exercise replacement engine recommending valid alternatives for unavailable equipment or joint discomfort.
  - In-app notification and smart reminder system for scheduled workouts.
  - High-fidelity downloadable PDF activity report generation.
- **Exit Criteria**:
  - Analytics accurately reflect actual logged database sets and reps.
  - Feedback directly alters subsequent workout recommendations.
  - Downloadable PDF compiles cleanly with proper branding and layout.
  - Phase 6 report posted and user approval received.

---

### Phase 7 — Testing, Production Deployment & Master Documentation
- **Deliverables**:
  - Comprehensive automated test suite:
    - Frontend unit & component tests (Vitest / React Testing Library).
    - Backend unit & integration tests (Pytest).
    - End-to-end user journey tests (Playwright).
    - WCAG AA accessibility audit (axe-core).
  - Production deployment of Next.js frontend to **Vercel**.
  - Production deployment of FastAPI backend to **Render** with health check probes.
  - Supabase production environment configuration (CORS, OAuth redirect URIs, production migrations).
  - Master `README.md`, setup guides, and architectural diagrams.
- **Exit Criteria**:
  - 100% test pass rate across all test suites.
  - Zero open TypeScript or linting errors.
  - Live production URLs verified and functional.
  - Complete documentation delivered.
  - Final project sign-off.
