# FitGuide AI 🏋️‍♂️⚡
> **An Athletic AI Fitness Companion & Workout Management Platform**  
> Engineered with Next.js 14 (App Router), Python FastAPI, Supabase PostgreSQL with `pgvector`, Gemini RAG Knowledge Retrieval, and Fine-Tuned ML Intent Routing.

[![Next.js 14](https://img.shields.io/badge/Next.js-14.2-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://python.org/)
[![Supabase pgvector](https://img.shields.io/badge/Supabase-pgvector-3ECF8E?logo=supabase)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. System Architecture

```
                                  HTTPS
               ATHLETE BROWSER ───────────────┐
                                               ▼
                                  ┌─────────────────────────┐
                                  │   Next.js 14 Frontend   │
                                  │   (Vercel Edge CDN)     │
                                  └────────────┬────────────┘
                                               │
                                               │ HTTPS / Bearer JWT
                                               ▼
                                  ┌─────────────────────────┐
                                  │  FastAPI Backend Worker │
                                  │  (Render / Railway)     │
                                  │  Python 3.12 + Uvicorn  │
                                  └────────────┬────────────┘
                                               │
                         ┌─────────────────────┴─────────────────────┐
                         ▼                                           ▼
            ┌─────────────────────────┐                 ┌─────────────────────────┐
            │   Supabase PostgreSQL   │                 │     Google Gemini API   │
            │ - Row-Level Security    │                 │ - 768-dim Embeddings    │
            │ - pgvector HNSW Index   │                 │ - Streaming SSE Chat    │
            │ - 84 Curated Exercises  │                 │ - Structured Pydantic   │
            └─────────────────────────┘                 └─────────────────────────┘
```

---

## 2. Core Capabilities

- **Clinical Safety Rules Engine**: Deterministic guardrails intercept red-flag symptoms (cardiac pain, dizziness/syncope, minor max-effort lifts, geriatric high-impact movements) before LLM invocation.
- **Biomechanical Exercise Library**: 84 verified exercises (`01_exercises.sql`) categorized by movement pattern, plane, primary/secondary muscles, and equipment requirements with video media.
- **RAG-Grounded AI Coach**: Real-time vector retrieval over authoritative exercise science guidelines (ACSM, WHO, NSCA, NIA, ISSN, CDC) generating verified inline citations (`[Source: ACSM Guidelines]`).
- **Real-Time ML Intent Routing**: 6-class intent classifier (`baseline_classifier.joblib`, 2.39ms p95 latency) accurately distinguishing workout generation, exercise substitution, injury triage, progress inquiries, and chit-chat.
- **Active Workout Player & Scheduler**: Interactive logging with set-by-set weight, RPE tracking, dynamic exercise substitution, and 7-day schedule management.
- **Restrained Progress Analytics & PDF Export**: Consistency score, accumulated volume load ($\sum \text{reps} \times \text{kg}$), anatomical muscle group distribution, AI retrospective coach, and publication-grade downloadable ReportLab PDF activity reports.

---

## 3. Urban Performance Design System

FitGuide AI implements an authentic athletic aesthetic built on restrained dark-mode tokens and technical typography:

| Token | Hex Value | Semantic Usage |
| :--- | :--- | :--- |
| **`carbon`** | `#171B18` | Deep matte background |
| **`forest`** | `#26372D` | Structural containers, cards, and borders |
| **`lime`** | `#C4E76B` | High-visibility athletic accent, primary buttons, active states |
| **`chalk`** | `#E8E5D9` | High-contrast technical typography |
| **`sand`** | `#B5A78D` | Secondary metadata and muted labels |
| **`burnt`** | `#C8794D` | Safety warnings, alerts, and red-flag indicators |

**Typography**: Space Grotesk (headings & numeric readouts) paired with Inter (data tables & body prose).

---

## 4. Monorepo Organization

```
fitguide-ai/
├── apps/
│   ├── api/                   # Python FastAPI Backend
│   │   ├── app/
│   │   │   ├── core/          # Safety rules, auth middleware, config
│   │   │   ├── data/          # 84-exercise catalog
│   │   │   ├── ml_artifacts/  # Embedded trained classifier model
│   │   │   ├── rag/           # Document ingestion, 768-dim embeddings, retrieval
│   │   │   ├── routers/v1/    # Health, Chat, Exercises, Workouts, Progress, Schedule
│   │   │   └── services/      # Gemini LLM, ReportLab PDF, Intent Router
│   │   ├── tests/             # 55 automated pytest suites
│   │   ├── Dockerfile         # Multi-stage hardened production container
│   │   └── requirements.txt
│   └── web/                   # Next.js 14 App Router Frontend
│       ├── src/
│       │   ├── app/           # 16 routes (Auth, Dashboard, Workouts, Exercises, Progress)
│       │   ├── components/    # Urban Performance UI primitives
│       │   └── lib/           # Supabase SSR client, API fetcher, utilities
│       ├── tests/             # Unit and utility tests
│       └── vercel.json        # Production Edge security headers
├── docs/                      # Architectural specs, API contracts, RLS policies
├── ml/                        # ML Fine-tuning pipeline (dataset, LoRA training, eval)
├── scripts/
│   ├── smoke_test.py          # Portable zero-dependency production verification harness
│   └── test_deep_audit.py     # 11-gate full-stack integration audit
├── supabase/
│   └── migrations/            # 001-005 PostgreSQL DDL, pgvector HNSW, RLS policies
├── DEPLOYMENT.md              # Production deployment runbook (Render, Vercel, Supabase)
└── render.yaml                # Infrastructure as Code specification for backend deployment
```

---

## 5. Local Development Setup

### Prerequisites
- Node.js >= 18.17 (v20+ recommended)
- Python >= 3.11 (3.12 recommended)
- A Supabase project (with PostgreSQL + `pgvector`)
- A Google Gemini API key

### Step 1: Clone & Configure Environment
```bash
git clone https://github.com/your-username/fitguide-ai.git
cd fitguide-ai
```

#### Backend Environment (`apps/api/.env`)
```ini
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_secret
SUPABASE_JWT_SECRET=your_jwt_secret
GEMINI_API_KEY=your_gemini_api_key
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000
```

#### Frontend Environment (`apps/web/.env.local`)
```ini
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_public_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 2: Run Database Migrations
In the Supabase SQL Editor, run scripts sequentially:
1. `supabase/migrations/001_initial_schema.sql`
2. `supabase/migrations/002_enable_pgvector.sql`
3. `supabase/migrations/003_rls_policies.sql`
4. `supabase/migrations/004_indexes.sql`
5. `supabase/migrations/005_grants.sql`
6. `supabase/seed/01_exercises.sql` (populates 84 curated exercises)

### Step 3: Start Services
```bash
# Terminal 1: Backend
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd apps/web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 6. Verification & Automated Test Suite

```bash
# 1. Backend Pytest Suite (55 tests)
cd apps/api
python -m pytest tests -v

# 2. Frontend Unit Tests (8 tests)
cd apps/web
npm run test

# 3. TypeScript Typecheck (0 errors)
cd apps/web
npm run typecheck

# 4. Deep Integration Audit (11 security & flow gates)
python scripts/test_deep_audit.py

# 5. Production Smoke Test Harness
python scripts/smoke_test.py --api-url http://localhost:8000
```

---

## 7. Production Deployment

See the comprehensive [DEPLOYMENT.md](DEPLOYMENT.md) runbook for step-by-step instructions:
- **Backend**: Containerized deployment on [Render](https://render.com) using `render.yaml` or `Dockerfile`.
- **Frontend**: Edge deployment on [Vercel](https://vercel.com) with security headers in `vercel.json`.
- **Database**: Managed PostgreSQL on [Supabase](https://supabase.com) with pgvector and Row-Level Security.

---

## 8. Clinical Disclaimer

FitGuide AI is an educational fitness and athletic workout companion designed for healthy individuals. It does not provide medical diagnoses, treatment plans, or clinical therapy. Users must consult a certified medical professional prior to commencing any high-intensity physical exertion.
