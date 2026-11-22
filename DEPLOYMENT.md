# FeedGuide AI — Production Deployment Guide & Runbook

This guide provides end-to-end instructions for deploying FeedGuide AI to production using **Vercel** (Next.js 14 Frontend), **Render or Railway** (FastAPI Backend), and **Supabase** (Managed PostgreSQL + pgvector + Auth).

---

## Architecture Topology

```
┌─────────────────────────────────┐
│     Athletic Client Browser     │
└───────────────┬─────────────────┘
                │
        HTTPS   │
                ▼
┌─────────────────────────────────┐        HTTPS / Bearer        ┌──────────────────────────────────┐
│      Next.js 14 Frontend        │ ───────────────────────────> │     FastAPI Python Backend       │
│     (Hosted on Vercel)          │                              │     (Hosted on Render/Railway)   │
│   https://feedguide.vercel.app  │                              │   https://api.feedguide.ai       │
└───────────────┬─────────────────┘                              └───────────────┬──────────────────┘
                │                                                                │
                │ Supabase Auth (OAuth & JWT)                     Service Role   │  pgvector / RLS
                └─────────────────────────────┬──────────────────────────────────┘
                                              ▼
                               ┌──────────────────────────────────┐
                               │       Supabase PostgreSQL        │
                               │  - Row Level Security (RLS)      │
                               │  - pgvector 768-dim Embeddings   │
                               │  - Curated Exercise Catalog (84) │
                               └──────────────────────────────────┘
```

---

## Prerequisites

1. **GitHub Account**: Containing the committed FeedGuide AI repository.
2. **Supabase Account**: A live Supabase project ([supabase.com](https://supabase.com)).
3. **Vercel Account**: Free or Pro tier ([vercel.com](https://vercel.com)).
4. **Render or Railway Account**: Free or Starter tier ([render.com](https://render.com) or [railway.app](https://railway.app)).
5. **Google Gemini API Key**: Free tier active from Google AI Studio.

---

## Step 1: Database Setup & Migrations (Supabase)

If not already executed during local development:

1. Log in to your **Supabase Dashboard** and open your project.
2. Navigate to the **SQL Editor**.
3. Sequentially run the migration files located in `supabase/migrations/`:
   - `001_initial_schema.sql` — Profiles, onboarding, and base schema.
   - `002_exercises_schema.sql` — Exercise catalog, muscle groups, equipment, and media tables.
   - `003_workouts_schedule_schema.sql` — Workout plans, sessions, exercise logs, and calendar entries.
   - `004_chat_feedback_schema.sql` — AI conversations, messages, usage telemetry, and reports.
   - `005_rag_pgvector.sql` — Enables `vector` extension, creates `knowledge_documents` and `knowledge_chunks` (768 dimensions with IVFFlat cosine indexing).
4. Populate the initial verified data by running the seeds in `supabase/seed/`:
   - `01_exercises.sql` — Inserts the 84 verified exercises with cited media.
   - `02_knowledge_docs.sql` — Inserts authoritative guidelines (ACSM, WHO, NSCA, NIA, ISSN, CDC).

---

## Step 2: Backend Deployment (Render)

### Option A: Using Infrastructure as Code (`render.yaml`)

1. Connect your GitHub repository to **Render**.
2. Create a new **Blueprint Instance** and point it to `render.yaml`.
3. Render will automatically detect the Python 3.12 environment and provision the `feedguide-api` web service.

### Option B: Manual Web Service Setup on Render

1. On the Render Dashboard, click **New + ➔ Web Service**.
2. Select your GitHub repository.
3. Configure the service settings:
   - **Name**: `feedguide-api`
   - **Region**: Closest to your users (e.g., Oregon, Frankfurt, Singapore)
   - **Branch**: `master`
   - **Root Directory**: `apps/api`
   - **Runtime**: `Python`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2 --proxy-headers --forwarded-allow-ips='*'`
   - **Health Check Path**: `/api/v1/health`
   - **Auto-Deploy**: `Yes`

4. Add the **Environment Variables** in the Render Environment tab:
   | Variable | Value | Source / Description |
   | :--- | :--- | :--- |
   | `ENV` | `production` | Enables production settings |
   | `PYTHON_VERSION` | `3.12.10` | Enforces Python 3.12 runtime |
   | `SUPABASE_URL` | `https://<your-id>.supabase.co` | From Supabase Project Settings ➔ API |
   | `SUPABASE_ANON_KEY` | `eyJ...` | Supabase Anon Public Key |
   | `SUPABASE_SERVICE_ROLE_KEY` | `eyJ...` | Supabase Service Role Secret |
   | `SUPABASE_JWT_SECRET` | `<your-jwt-secret>` | Supabase Project Settings ➔ API ➔ JWT Secret |
   | `GEMINI_API_KEY` | `<your-gemini-key>` | Google AI Studio Gemini API Key |
   | `CORS_ORIGINS` | `https://<your-frontend>.vercel.app,http://localhost:3000` | Allowed frontend origins (comma-separated) |
   | `CHAT_RATE_LIMIT_PER_MINUTE` | `15` | AI Rate Limiter threshold |

5. Click **Create Web Service**. Wait for the build to finish. Once live, note your backend URL (e.g. `https://feedguide-api.onrender.com`).

---

## Step 3: Frontend Deployment (Vercel)

1. Log in to **Vercel** and click **Add New... ➔ Project**.
2. Import your GitHub repository.
3. Configure the build settings:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click *Edit* and select `apps/web`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

4. Configure the **Environment Variables** in Vercel:
   | Variable | Value | Description |
   | :--- | :--- | :--- |
   | `NEXT_PUBLIC_SUPABASE_URL` | `https://<your-id>.supabase.co` | Supabase endpoint URL |
   | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` | Supabase public anon key |
   | `NEXT_PUBLIC_API_BASE_URL` | `https://feedguide-api.onrender.com/api/v1` | URL of your deployed Render backend |
   | `NEXT_PUBLIC_APP_URL` | `https://<your-project>.vercel.app` | Your production Vercel domain |

5. Click **Deploy**. Vercel will build all 16 static and dynamic routes.
6. Once deployed, note your production frontend URL (e.g., `https://feedguide-ai.vercel.app`).

---

## Step 4: Supabase Production Authentication Configuration

To ensure OAuth logins (Google) and email confirmations redirect back to your live production frontend:

1. Open your **Supabase Dashboard**.
2. Go to **Authentication ➔ URL Configuration**.
3. Set the **Site URL**:
   ```
   https://<your-project>.vercel.app
   ```
4. In **Redirect URLs**, click **Add URL** and add:
   ```
   https://<your-project>.vercel.app/**
   https://<your-project>.vercel.app/auth/callback
   ```
5. *(If using Google OAuth)*:
   - Go to your **Google Cloud Console ➔ APIs & Services ➔ Credentials**.
   - Open your OAuth 2.0 Client ID.
   - Ensure the **Authorized redirect URIs** includes:
     ```
     https://<your-supabase-id>.supabase.co/auth/v1/callback
     ```

---

## Step 5: Post-Deployment Smoke Verification

Run the automated smoke test script locally against your live production endpoints to verify end-to-end system health:

```bash
python scripts/smoke_test.py --api-url https://feedguide-api.onrender.com --web-url https://feedguide-ai.vercel.app
```

### Expected Output:
```
======================================================================
FEEDGUIDE AI — PRODUCTION SMOKE TEST SUITE
Target API Endpoint: https://feedguide-api.onrender.com
Target Web Endpoint: https://feedguide-ai.vercel.app
======================================================================
  [PASS] API Health Probe (185.2ms) -> HTTP 200
  [PASS] API Root Index (112.4ms) -> HTTP 200
  [PASS] Exercise Catalog (>= 80 records) (142.1ms) -> HTTP 200
         Verified catalog integrity: 84 exercises loaded.
  [PASS] ML Intent Classification (< 20ms) (15.4ms) -> HTTP 200
         Predicted intent: 'workout_request' -> Target: 'structured_workout_engine'
  [PASS] Security Boundary (Unauthorized Rejection) (98.6ms) -> HTTP 401 (Expected Security Rejection)
  [PASS] Frontend Web Landing Page (210.8ms) -> HTTP 200

======================================================================
RESULTS: 7/7 Checks Passed (100.0%)
======================================================================
[SUCCESS] All production smoke checks passed! Deployment is verified.
```

---

## Operational Maintenance

- **Worker Scaling**: FastAPI runs with `--workers 2` by default. For higher throughput, increase worker concurrency in `render.yaml` or container env.
- **Security Updates**: All security headers (`X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`) are baked into `apps/web/vercel.json`.
- **Zero Downtime Deploys**: Both Vercel and Render perform atomic blue/green deployments with health check gating at `/api/v1/health`.
