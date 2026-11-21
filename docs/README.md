# FeedGuide AI — Architecture & Planning Documentation (Phase 0)

Welcome to the architectural specification for **FeedGuide AI**, a secure, responsive, high-performance digital fitness companion and workout management platform.

This directory contains the complete Phase 0 system architecture, database schema, API contracts, security models, safety specifications, and design system.

---

## Documentation Index

1. [Architecture & Stack Decisions](requirements_and_decisions.md)
   - Product requirements analysis
   - Stack selection & rationale (Next.js, FastAPI, Supabase, Render, Gemini/OpenAI, pgvector)
   - Monorepo directory structure & service boundaries

2. [Sitemap, Page Hierarchy & UX States](sitemap_and_navigation.md)
   - Complete route tree & access levels
   - Desktop rail/sidebar vs. mobile bottom tab navigation
   - State specifications: Loading (skeletons), Empty, Error, and Success states

3. [Database Schema, ERD & RLS Security](schema_and_rls.md)
   - Entity-Relationship Diagram (Mermaid)
   - PostgreSQL table definitions with constraints, types, and indexes
   - Row-Level Security (RLS) policies and verification matrix

4. [API Contract Specification](api.md)
   - Versioned REST API (`/api/v1/...`)
   - Complete endpoint schemas, request/response models, pagination, and error envelopes
   - JWT authentication verification and token-derived user identity

5. [Safety Rules & Clinical Guardrails Specification](safety_rules.md)
   - Versioned `safety_rules` module specification
   - Age-based constraints (minors < 18, adults 18–64, older adults 65+)
   - Clinical red flag detection (chest pain, dizziness, severe injury, eating disorders)
   - Defensive prompt injection boundaries & user disclaimer policy

6. [AI Architecture, RAG Pipeline & Fine-Tuning](ai_rag_finetuning.md)
   - Provider-agnostic LLM service interface
   - Context builder for compact, token-efficient user grounding
   - Pydantic structured output validation and automatic repair
   - Curated RAG pipeline (chunking, 768-dim embeddings, pgvector HNSW search, citation engine)
   - Fitness-Intent Classification fine-tuning experiment (LoRA/PEFT, dataset spec, evaluation harness)

7. [Design System & UI Tokens](design_system.md)
   - Brand identity: *Urban Performance / Premium Athletic*
   - Strict palette tokens (`#171B18`, `#26372D`, `#C4E76B`, `#E8E5D9`, `#B5A78D`, `#C8794D`)
   - Typography scale (Space Grotesk + Inter) and layout geometry
   - Component inventory, chart styling, motion guidelines, and authentic media credits

8. [Implementation Plan & Phase Exit Criteria](implementation_plan.md)
   - Sequential roadmaps for Phases 0 through 7
   - Strict definition of done and verification gates per phase
   - Testing strategies (unit, integration, RLS, E2E)

9. [Credentials & Environment Configuration](credentials_and_env.md)
   - Required environment variables for frontend and backend
   - Third-party service configurations (Supabase, Render/Fly, Google Cloud/OpenAI)
   - Step-by-step setup instructions for project launch
