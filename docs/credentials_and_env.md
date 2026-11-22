# Section 9: Credentials & Environment Configuration Guide

To preserve absolute security, secrets are stored exclusively in environment variables and are never committed to version control. The client browser has zero access to database service-role secrets or LLM provider API keys.

---

## 1. Master List of Required Credentials

The user must configure the following service credentials across the project lifecycle:

| Service | Credential Name | Scope | Description & Where to Obtain |
| :--- | :--- | :--- | :--- |
| **Supabase** | `NEXT_PUBLIC_SUPABASE_URL` | Frontend & Backend | The base REST/PostgreSQL project URL from the Supabase Project Dashboard (`Settings -> API`). |
| **Supabase** | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Frontend Only | The public anonymous API key for client-side authentication and public read operations. |
| **Supabase** | `SUPABASE_SERVICE_ROLE_KEY` | Backend Only | High-privilege service-role key for backend admin tasks, RAG embeddings ingestion, and seeding. **Never expose to web client.** |
| **Supabase** | `SUPABASE_JWT_SECRET` | Backend Only | The HMAC secret used by FastAPI to verify Supabase JWT signatures on incoming requests (`Settings -> API -> JWT Secret`). |
| **Google Cloud / AI Studio** | `GEMINI_API_KEY` | Backend Only | API key for Google Gemini LLM (`gemini-1.5-flash`, `gemini-1.5-pro`) and `text-embedding-004`. Obtained from Google AI Studio. |
| **OpenAI (Optional Fallback)** | `OPENAI_API_KEY` | Backend Only | Optional fallback LLM key (`gpt-4o-mini`) from OpenAI platform. |
| **Google Cloud (OAuth)** | `GOOGLE_CLIENT_ID` / `SECRET` | Supabase Dashboard | Configured in Supabase Auth Providers for Google OAuth sign-in. |

---

## 2. Frontend Environment File (`apps/web/.env.example`)

```bash
# Supabase Public Configuration
NEXT_PUBLIC_SUPABASE_URL="https://your-project-ref.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-anon-token..."

# Backend API Base URL
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api/v1"

# Application URL
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

---

## 3. Backend Environment File (`apps/api/.env.example`)

```bash
# Server Configuration
ENV="development"
PORT=8000
HOST="0.0.0.0"
CORS_ORIGINS="http://localhost:3000,https://fitguide.vercel.app"

# Supabase Database & Auth Configuration
SUPABASE_URL="https://your-project-ref.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-service-role-key..."
SUPABASE_JWT_SECRET="your-supabase-jwt-secret-here-minimum-32-chars"
DATABASE_URL="postgresql://postgres:your-db-password@db.your-project-ref.supabase.co:5432/postgres"

# LLM & Embedding Services
PRIMARY_LLM_PROVIDER="gemini" # Options: "gemini" | "openai"
GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere..."
OPENAI_API_KEY="" # Optional fallback

EMBEDDING_PROVIDER="gemini" # Options: "gemini" | "sentence_transformers"
EMBEDDING_MODEL_NAME="text-embedding-004"
VECTOR_DIMENSION=768

# Rate Limiting
CHAT_RATE_LIMIT_PER_MINUTE=15

# Security
APP_SECRET_KEY="generate-a-secure-random-32-character-secret"
```

---

## 4. Supabase Project Setup Checklist

1. **Create Supabase Project**:
   - Go to [Supabase](https://supabase.com) and create a new project named `fitguide-ai`.
   - Save the Database Password securely.
2. **Enable Vector Extension**:
   - Navigate to `Database -> Extensions` and verify `vector` is enabled.
3. **Configure Authentication Providers**:
   - Go to `Authentication -> Providers`.
   - Ensure **Email** is enabled with "Confirm email" toggled on.
   - (Optional for Google OAuth) Enable **Google**, enter your Google OAuth Client ID and Secret obtained from the Google Cloud Console. Set Redirect URL to `https://your-project-ref.supabase.co/auth/v1/callback`.
4. **Retrieve Keys**:
   - Copy Project URL, Anon Key, Service Role Key, and JWT Secret from `Project Settings -> API`.
