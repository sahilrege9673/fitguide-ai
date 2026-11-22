# Section 1: Requirements Analysis & Final Stack Decisions

## 1. Executive Summary & Product Requirements

**FitGuide AI** is an intelligent, personalized digital fitness companion and workout management platform engineered to deliver age-appropriate, grounded fitness planning, progress analytics, and interactive coaching.

Unlike generic fitness chatbots or template-driven workout generators, FitGuide AI grounds every decision, recommendation, and chat response in:
1. The user's verified onboarding profile (age group, fitness goals, experience level, workout location, available equipment, preferred activities, available time, preferred workout days).
2. Their active weekly schedule and recovery status.
3. Their real completed workout session logs and historical feedback.
4. Curated, evidence-based exercise science principles retrieved via an authoritative RAG pipeline.

### Core Product Modules

| Module | Core Functionality |
| :--- | :--- |
| **Auth & Security** | Supabase Auth (Email/Password + Google OAuth), email verification, password reset, JWT verification on FastAPI backend with strict Row Level Security (RLS). User identity strictly extracted from JWT `sub` claim. |
| **Onboarding** | Multi-step interactive flow with auto-save progress, collecting biological age group, goals, experience, location, equipment, time budget, and day preferences. Includes explicit medical/fitness safety disclaimers. |
| **Dashboard** | Daily briefing, today's prescribed workout, upcoming schedule, weekly completion metrics, streak tracking, and personalized AI recommendations based on recent activity. |
| **My Workouts** | Structured daily routines, exercise instructions, target sets/reps/duration, real-time logging, exercise swap/alternative recommendations, and historical session review. |
| **Exercise Library** | Comprehensive searchable and filterable database (>= 80 verified exercises) by muscle group, equipment, category, difficulty, and age suitability, with cited demonstration media. |
| **AI Assistant** | Real-time streaming chat grounded in the user's live profile, schedule, and workout logs. Enforces clinical safety boundaries, provides citation-backed guidance, and maintains persistent conversation history. |
| **My Schedule** | Interactive weekly calendar view, active days vs. programmed recovery, schedule shifting, workout rescheduling, and automated reminders. |
| **My Progress** | Restrained analytical dashboards (weekly/monthly volume, consistency index, muscle-group distribution), AI-generated progress retrospectives, and downloadable PDF activity summaries. |
| **My Profile** | Personal account management, fitness preference adjustments, GDPR/CCPA data export (JSON), and complete account deletion with cascade cleanup. |
| **Safety Engine** | Versioned, deterministic code module preventing medical diagnosis, treatment claims, extreme caloric restriction, max-effort lifts for minors, and unsafe training during injury/pain signals. |

---

## 2. Final Stack Decisions & Architectural Rationale

To achieve production-grade reliability, sub-second API latency, strict user data isolation, and cost-effective scalability, the following stack decisions are finalized:

### 2.1 Backend Hosting: **Render** (with Railway as secondary deployment target)

- **Selected**: **Render Web Service** (Native Python / Docker runtime)
- **Alternatives Evaluated**:
  - *Railway*: Flexible and developer-friendly, but unpredictable pricing spikes, dynamic usage charges, and frequent tier policy changes create budget unpredictability.
  - *Fly.io*: Superior edge performance via Firecracker microVMs, but introduces operational complexity (WireGuard networking, custom volume management, dedicated IPv4 surcharge, complex DNS routing).
- **Decision Rationale**:
  1. **Monorepo Compatibility**: Render natively supports monorepos by specifying `Root Directory: apps/api` and custom build commands.
  2. **Predictable Managed Environment**: Transparent standard pricing, automated TLS/SSL provisioning, continuous deployment from GitHub branch pushes, and zero configuration container builds.
  3. **Zero Cold-Start on Paid/Standard Tier**: Guarantees fast response times for backend API consumers and webhook listeners.
  4. **Health Check Probing**: Built-in HTTP health check polling on `/api/v1/health` with automated zero-downtime rolling deploys.

### 2.2 LLM Provider: **Google Gemini API** (with OpenAI fallback adapter)

- **Selected Primary**: **Google Gemini API** (`gemini-1.5-flash` for high-throughput sub-second chat & structured extraction; `gemini-1.5-pro` for complex weekly schedule generation and analytical retrospectives)
- **Interface**: Provider-agnostic abstract interface (`LLMProvider`) located in `apps/api/app/services/llm/base.py`, allowing drop-in swapping of OpenAI (`gpt-4o-mini` / `gpt-4o`) via environment configuration.
- **Decision Rationale**:
  1. **Sub-second Latency**: `gemini-1.5-flash` delivers industry-leading time-to-first-token (TTFT), critical for interactive streaming fitness coaching.
  2. **Strict Structured JSON Support**: Native JSON Schema enforcement guarantees that workout recommendations adhere strictly to Pydantic models referencing valid exercise database IDs.
  3. **Generous Context Window**: Allows comprehensive multi-session user history and RAG chunks to be ingested without truncation.
  4. **Cost Efficiency**: High rate limits and low inference costs make it sustainable for long chat sessions.

### 2.3 Embeddings & Vector Dimension: **Google text-embedding-004 (768 Dimensions)**

- **Selected**: **Google `text-embedding-004`** (Vector dimension: **768**)
- **Local / Self-Hosted Fallback**: `sentence-transformers` using `BAAI/bge-base-en-v1.5` or `sentence-transformers/all-mpnet-base-v2` (both native 768 dimensions).
- **Decision Rationale**:
  1. **768-Dimension Standard**: 768 dimensions provide an optimal balance between semantic representation fidelity, HNSW index build time, memory footprint, and query latency in pgvector.
  2. **Local/Cloud Parity**: Because both `text-embedding-004` and `bge-base-en-v1.5` share the exact 768-dimension size, database migrations in Supabase fix the vector dimension at `VECTOR(768)`. The system can switch between local open-source sentence-transformers (for offline testing/evaluation) and cloud APIs with zero schema migration or index rebuild.

### 2.4 Database & Vector Storage: **Supabase PostgreSQL + pgvector**

- **Selected**: Supabase Managed PostgreSQL 15+ with `pgvector` extension.
- **Decision Rationale**:
  1. **Unified Storage**: Combines relational user profiles, workout plans, and schedule entities with high-dimensional vector embeddings in a single ACID-compliant database.
  2. **Row-Level Security (RLS)**: Enforces cryptographic data isolation at the engine level. Even if an API endpoint suffered a parameter injection bug, Postgres prohibits accessing other users' rows.
  3. **HNSW Vector Indexing**: Hierarchical Navigable Small World indexes enable sub-10ms cosine similarity searches with zero extra vector database infrastructure (e.g., Pinecone/Milvus).

### 2.5 Frontend Framework: **Next.js 14+ (App Router, TypeScript, Tailwind CSS)**

- **Deployment**: **Vercel**
- **Decision Rationale**:
  1. **Server Components & Edge Streaming**: Server-rendered dashboard shell for instant First Contentful Paint (FCP) combined with client-side streaming chat.
  2. **Strict TypeScript & Zod Validation**: End-to-end type safety shared with FastAPI schemas.
  3. **Tailwind CSS Design Tokens**: Exact mapping of the Urban Performance palette without runtime CSS overhead.

---

## 3. Monorepo Architecture & Directory Boundaries

The codebase is organized as a clean, decoupled monorepo:

```
fitguide-ai/
├── apps/
│   ├── web/                           # Next.js 14+ App Router frontend
│   │   ├── public/                    # Static assets, certified exercise SVGs/placeholders
│   │   ├── src/
│   │   │   ├── app/                   # App Router pages and layouts
│   │   │   │   ├── (auth)/            # Auth routes (login, register, forgot-password, reset)
│   │   │   │   ├── (onboarding)/      # Multi-step onboarding flow
│   │   │   │   ├── (dashboard)/       # Authenticated app shell
│   │   │   │   │   ├── dashboard/     # Daily briefing & stats
│   │   │   │   │   ├── workouts/      # Workout list, daily view, active tracking
│   │   │   │   │   ├── exercises/     # Exercise library & exercise detail
│   │   │   │   │   ├── assistant/     # AI Assistant interactive chat
│   │   │   │   │   ├── schedule/      # Weekly calendar & adjustments
│   │   │   │   │   ├── progress/      # Analytics, retrospectives & PDF export
│   │   │   │   │   └── profile/       # Profile, preferences, data export/delete
│   │   │   │   ├── api/               # Next.js API routes (client-side proxies if needed)
│   │   │   │   ├── layout.tsx         # Root layout (Space Grotesk + Inter font injection)
│   │   │   │   └── page.tsx           # High-impact landing page
│   │   │   ├── components/            # Reusable UI component library
│   │   │   │   ├── ui/                # Base primitives (Button, Card, Input, Modal, Badge, etc.)
│   │   │   │   ├── layout/            # Desktop sidebar, mobile bottom nav, header, breadcrumbs
│   │   │   │   ├── feedback/          # Skeletons, empty states, error banners, toasts
│   │   │   │   └── charts/            # Custom SVG/Canvas restrained athletic charts
│   │   │   ├── features/              # Modular feature domains
│   │   │   │   ├── auth/              # Auth forms, Supabase session handlers
│   │   │   │   ├── onboarding/        # Step-by-step form state & persist logic
│   │   │   │   ├── workouts/          # Workout player, logger, exercise swapper
│   │   │   │   ├── chat/              # Streaming chat UI, message parser, citations
│   │   │   │   └── progress/          # Metric aggregators, report generator
│   │   │   ├── lib/
│   │   │   │   ├── api/               # Typed Axios/Fetch client with Supabase JWT interceptor
│   │   │   │   ├── supabase/          # Supabase browser, server, and middleware clients
│   │   │   │   └── utils/             # Formatters, date math, cn() class merger
│   │   │   └── types/                 # Shared TypeScript models (mirrors Pydantic)
│   │   ├── tailwind.config.ts         # Design system tokens, typography & spacing
│   │   ├── tsconfig.json              # Strict TypeScript configuration
│   │   └── package.json
│   │
│   └── api/                           # Python FastAPI Backend
│       ├── app/
│       │   ├── core/                  # Core infrastructure
│       │   │   ├── config.py          # Pydantic Settings, environment validation
│       │   │   ├── security.py        # Supabase JWT verification, CORS, rate limiters
│       │   │   ├── database.py        # Async SQLAlchemy / Supabase connection pool
│       │   │   └── safety_rules.py    # Clinical & age-appropriate safety rules engine
│       │   ├── schemas/               # Pydantic v2 validation contracts
│       │   │   ├── auth.py            # User identity, token payload schemas
│       │   │   ├── profile.py         # Onboarding & preferences schemas
│       │   │   ├── exercise.py        # Exercise catalog & media schemas
│       │   │   ├── workout.py         # Workout plan, session & exercise log schemas
│       │   │   ├── chat.py            # Chat messages, streaming chunk schemas
│       │   │   └── progress.py        # Analytics, summary & report schemas
│       │   ├── services/              # Business logic layer
│       │   │   ├── profile_service.py # User profile & preferences persistence
│       │   │   ├── exercise_service.py# Search, filter & exercise swapper
│       │   │   ├── workout_service.py # Deterministic workout generator & tracker
│       │   │   ├── schedule_service.py# Calendar management & recovery day balance
│       │   │   ├── report_service.py  # Analytics aggregation & PDF generation
│       │   │   └── llm/               # LLM abstraction layer
│       │   │       ├── base.py        # Abstract LLMProvider interface
│       │   │       ├── gemini.py      # Google Gemini implementation
│       │   │       └── openai.py      # OpenAI fallback implementation
│       │   ├── rag/                   # Retrieval-Augmented Generation subsystem
│       │   │   ├── ingest.py          # Document loader & Markdown/PDF parser
│       │   │   ├── chunker.py         # Token-aware text chunker (300-500 tokens)
│       │   │   ├── embeddings.py      # Vector embedding generator (768-dim)
│       │   │   ├── retriever.py       # pgvector cosine similarity search + metadata filters
│       │   │   └── generator.py       # Grounded prompt construction & citation injector
│       │   ├── ml/                    # Fine-Tuning & Local Inference
│       │   │   ├── intent_classifier.py # Fine-tuned routing classifier loader
│       │   │   └── router.py          # AI query intent router
│       │   └── routers/               # Versioned REST controllers
│       │       ├── v1/
│       │       │   ├── auth.py        # Current user profile sync
│       │       │   ├── onboarding.py  # Preferences save & validation
│       │       │   ├── exercises.py   # Exercise search, filters, detail
│       │       │   ├── workouts.py    # Plan generation, logging, history
│       │       │   ├── schedule.py    # Calendar schedule CRUD
│       │       │   ├── chat.py        # Context-aware chat & stream
│       │       │   ├── progress.py    # Trends, summaries & PDF export
│       │       │   └── health.py      # Liveness & readiness probes
│       ├── tests/                     # Pytest suite
│       │   ├── unit/                  # Safety rules, chunker, schema tests
│       │   ├── integration/           # FastAPI router integration tests
│       │   └── rag/                   # Retrieval benchmark & hit-rate tests
│       ├── requirements.txt           # Pinned dependencies
│       ├── Dockerfile                 # Multi-stage production container build
│       └── main.py                    # ASGI application entrypoint
│
├── supabase/
│   ├── migrations/                    # Forward-only SQL migrations (Schema, RLS, Indexes)
│   │   ├── 001_initial_schema.sql     # Core tables & enum types
│   │   ├── 002_enable_pgvector.sql    # pgvector extension & 768-dim table
│   │   ├── 003_rls_policies.sql       # Strict Row Level Security policies
│   │   └── 004_indexes.sql            # Performance & HNSW vector indexes
│   ├── seed/                          # Seed datasets
│   │   ├── 01_exercises.sql           # >= 80 verified exercises with media citations
│   │   └── 02_knowledge_base.sql      # Curated exercise science reference documents
│   └── tests/                         # SQL policy verification test scripts
│
├── ml/
│   ├── data/                          # Labeled dataset for intent classification
│   │   ├── train.jsonl
│   │   ├── val.jsonl
│   │   └── test.jsonl
│   ├── train/
│   │   └── train_lora.py              # Hugging Face Transformers + PEFT/LoRA training script
│   ├── eval/
│   │   └── evaluate_model.py          # Confusion matrix, macro-F1, baseline comparisons
│   └── reports/                       # Documented fine-tuning experiment report
│
└── docs/                              # Comprehensive architecture & phase deliverables
    ├── README.md                      # Documentation Index
    ├── requirements_and_decisions.md  # Requirements & Decisions (this file)
    ├── sitemap_and_navigation.md      # Sitemap & Navigation Architecture
    ├── schema_and_rls.md              # Database Schema, ERD & Security
    ├── api.md                         # OpenAPI Contract Specifications
    ├── safety_rules.md                # Safety & Guardrail Specifications
    ├── ai_rag_finetuning.md           # AI, RAG & Fine-Tuning Specifications
    ├── design_system.md               # Design System, Tokens & UI Specifications
    ├── implementation_plan.md         # Phased Implementation Plan & Exit Criteria
    └── credentials_and_env.md         # Environment Variables & Setup Guide
```
