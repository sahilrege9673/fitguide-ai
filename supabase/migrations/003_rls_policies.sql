-- ==============================================================================
-- FitGuide AI — Migration 003: Row-Level Security (RLS) Policies
-- ==============================================================================

-- Enable RLS on every table
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.onboarding_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_media ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workout_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workout_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.session_exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exercise_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.schedule_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.knowledge_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_usage_log ENABLE ROW LEVEL SECURITY;

-- -----------------------------------------------------------------------------
-- 1. PROFILES POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert their own profile"
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- -----------------------------------------------------------------------------
-- 2. ONBOARDING PREFERENCES POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own preferences"
    ON public.onboarding_preferences FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own preferences"
    ON public.onboarding_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own preferences"
    ON public.onboarding_preferences FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own preferences"
    ON public.onboarding_preferences FOR DELETE
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 3. EXERCISES & MEDIA (Public Read-Only)
-- -----------------------------------------------------------------------------
CREATE POLICY "Anyone can view exercises"
    ON public.exercises FOR SELECT
    USING (true);

CREATE POLICY "Anyone can view exercise media"
    ON public.exercise_media FOR SELECT
    USING (true);

-- -----------------------------------------------------------------------------
-- 4. WORKOUT PLANS POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own workout plans"
    ON public.workout_plans FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own workout plans"
    ON public.workout_plans FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own workout plans"
    ON public.workout_plans FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own workout plans"
    ON public.workout_plans FOR DELETE
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 5. WORKOUT SESSIONS POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own workout sessions"
    ON public.workout_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own workout sessions"
    ON public.workout_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own workout sessions"
    ON public.workout_sessions FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own workout sessions"
    ON public.workout_sessions FOR DELETE
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 6. SESSION EXERCISES POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view session exercises of their own sessions"
    ON public.session_exercises FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions ws
            WHERE ws.id = session_exercises.session_id AND ws.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert session exercises into their own sessions"
    ON public.session_exercises FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.workout_sessions ws
            WHERE ws.id = session_exercises.session_id AND ws.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update session exercises of their own sessions"
    ON public.session_exercises FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions ws
            WHERE ws.id = session_exercises.session_id AND ws.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete session exercises of their own sessions"
    ON public.session_exercises FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.workout_sessions ws
            WHERE ws.id = session_exercises.session_id AND ws.user_id = auth.uid()
        )
    );

-- -----------------------------------------------------------------------------
-- 7. EXERCISE LOGS POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own exercise logs"
    ON public.exercise_logs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own exercise logs"
    ON public.exercise_logs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own exercise logs"
    ON public.exercise_logs FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own exercise logs"
    ON public.exercise_logs FOR DELETE
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 8. SCHEDULE ENTRIES POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own schedule entries"
    ON public.schedule_entries FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own schedule entries"
    ON public.schedule_entries FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own schedule entries"
    ON public.schedule_entries FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own schedule entries"
    ON public.schedule_entries FOR DELETE
    USING (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 9. FEEDBACK POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own feedback"
    ON public.feedback FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own feedback"
    ON public.feedback FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own feedback"
    ON public.feedback FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 10. CONVERSATIONS & MESSAGES POLICIES
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own conversations"
    ON public.conversations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own conversations"
    ON public.conversations FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own conversations"
    ON public.conversations FOR DELETE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can view their own messages"
    ON public.messages FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own messages"
    ON public.messages FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- -----------------------------------------------------------------------------
-- 11. KNOWLEDGE BASE (Public Read-Only)
-- -----------------------------------------------------------------------------
CREATE POLICY "Anyone can view knowledge documents"
    ON public.knowledge_documents FOR SELECT
    USING (true);

CREATE POLICY "Anyone can view knowledge chunks"
    ON public.knowledge_chunks FOR SELECT
    USING (true);

-- -----------------------------------------------------------------------------
-- 12. REPORTS & AI USAGE LOG
-- -----------------------------------------------------------------------------
CREATE POLICY "Users can view their own reports"
    ON public.reports FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own reports"
    ON public.reports FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own ai usage"
    ON public.ai_usage_log FOR SELECT
    USING (auth.uid() = user_id);
