-- ==============================================================================
-- FitGuide AI — Migration 004: Performance & HNSW Vector Indexes
-- ==============================================================================

-- 1. HNSW Vector Index for Knowledge Chunks (Cosine Distance)
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_embedding_hnsw 
ON public.knowledge_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 2. Foreign Key & Filter Indexes
CREATE INDEX IF NOT EXISTS idx_onboarding_preferences_user ON public.onboarding_preferences(user_id);
CREATE INDEX IF NOT EXISTS idx_workout_sessions_user_status ON public.workout_sessions(user_id, status);
CREATE INDEX IF NOT EXISTS idx_workout_sessions_scheduled ON public.workout_sessions(user_id, scheduled_time);
CREATE INDEX IF NOT EXISTS idx_session_exercises_session ON public.session_exercises(session_id);
CREATE INDEX IF NOT EXISTS idx_exercise_logs_session_exercise ON public.exercise_logs(session_exercise_id);
CREATE INDEX IF NOT EXISTS idx_exercise_logs_user ON public.exercise_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_schedule_entries_user_date ON public.schedule_entries(user_id, scheduled_date);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON public.messages(conversation_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_exercises_category_difficulty ON public.exercises(category, difficulty);
CREATE INDEX IF NOT EXISTS idx_exercises_slug ON public.exercises(slug);
