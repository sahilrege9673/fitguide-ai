-- ==============================================================================
-- FeedGuide AI — Migration 002: pgvector & Knowledge Base
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "vector";

-- 1. Knowledge Documents Reference Table
CREATE TABLE IF NOT EXISTS public.knowledge_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_url TEXT NOT NULL,
    license TEXT NOT NULL,
    category TEXT NOT NULL,
    published_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 2. Knowledge Chunks Table (Fixed 768 Dimensions)
CREATE TABLE IF NOT EXISTS public.knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES public.knowledge_documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
