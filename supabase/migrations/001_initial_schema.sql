-- ==============================================================================
-- FitGuide AI — Migration 001: Initial Schema
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Enums
DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('user', 'admin');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE age_group_enum AS ENUM ('minor_under_18', 'adult_18_64', 'senior_65_plus');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE experience_level_enum AS ENUM ('beginner', 'intermediate', 'advanced');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE workout_status_enum AS ENUM ('scheduled', 'in_progress', 'completed', 'skipped');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE schedule_entry_type AS ENUM ('workout', 'active_recovery', 'rest_day');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE sender_role_enum AS ENUM ('user', 'assistant', 'system');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE media_type_enum AS ENUM ('image', 'gif', 'video');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 2. Profiles Table (syncs with auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    role user_role DEFAULT 'user' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Trigger to automatically create profile row on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, role)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', ''),
        'user'
    )
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 3. Onboarding Preferences Table
CREATE TABLE IF NOT EXISTS public.onboarding_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES public.profiles(id) ON DELETE CASCADE,
    age_group age_group_enum NOT NULL,
    experience_level experience_level_enum NOT NULL,
    fitness_goals TEXT[] NOT NULL DEFAULT '{}',
    workout_location TEXT NOT NULL,
    available_equipment TEXT[] NOT NULL DEFAULT '{}',
    preferred_activities TEXT[] NOT NULL DEFAULT '{}',
    time_availability_mins INT NOT NULL CHECK (time_availability_mins BETWEEN 10 AND 180),
    preferred_days INT[] NOT NULL CHECK (array_length(preferred_days, 1) BETWEEN 1 AND 7),
    disclaimer_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 4. Exercises Reference Table
CREATE TABLE IF NOT EXISTS public.exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty experience_level_enum NOT NULL,
    primary_muscles TEXT[] NOT NULL DEFAULT '{}',
    secondary_muscles TEXT[] NOT NULL DEFAULT '{}',
    equipment_needed TEXT[] NOT NULL DEFAULT '{}',
    suitable_age_groups age_group_enum[] NOT NULL DEFAULT '{adult_18_64}',
    instructions TEXT NOT NULL,
    tips TEXT,
    contraindications TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 5. Exercise Media Table
CREATE TABLE IF NOT EXISTS public.exercise_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exercise_id UUID NOT NULL REFERENCES public.exercises(id) ON DELETE CASCADE,
    media_type media_type_enum NOT NULL,
    url TEXT NOT NULL,
    thumbnail_url TEXT,
    license_type TEXT NOT NULL,
    attribution_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 6. Workout Plans Table
CREATE TABLE IF NOT EXISTS public.workout_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    cycle_type TEXT NOT NULL DEFAULT 'weekly',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 7. Workout Sessions Table
CREATE TABLE IF NOT EXISTS public.workout_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    plan_id UUID REFERENCES public.workout_plans(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    focus_area TEXT NOT NULL,
    planned_duration_mins INT NOT NULL,
    scheduled_time TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    status workout_status_enum NOT NULL DEFAULT 'scheduled',
    perceived_exertion INT CHECK (perceived_exertion BETWEEN 1 AND 10),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 8. Session Exercises Table
CREATE TABLE IF NOT EXISTS public.session_exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.workout_sessions(id) ON DELETE CASCADE,
    exercise_id UUID NOT NULL REFERENCES public.exercises(id) ON DELETE RESTRICT,
    exercise_order INT NOT NULL,
    target_sets INT NOT NULL CHECK (target_sets > 0),
    target_reps INT,
    target_duration_secs INT,
    target_rest_secs INT DEFAULT 60,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE
);

-- 9. Exercise Logs Table
CREATE TABLE IF NOT EXISTS public.exercise_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_exercise_id UUID NOT NULL REFERENCES public.session_exercises(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    set_number INT NOT NULL,
    weight_kg NUMERIC(6, 2) DEFAULT 0.0,
    reps_performed INT,
    duration_seconds INT,
    rpe INT CHECK (rpe BETWEEN 1 AND 10),
    logged_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 10. Schedule Entries Table
CREATE TABLE IF NOT EXISTS public.schedule_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    session_id UUID REFERENCES public.workout_sessions(id) ON DELETE SET NULL,
    scheduled_date DATE NOT NULL,
    entry_type schedule_entry_type NOT NULL,
    title TEXT NOT NULL,
    is_rest_day BOOLEAN NOT NULL DEFAULT FALSE,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 11. Feedback Table
CREATE TABLE IF NOT EXISTS public.feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL UNIQUE REFERENCES public.workout_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    energy_rating INT NOT NULL CHECK (energy_rating BETWEEN 1 AND 5),
    difficulty_rating INT NOT NULL CHECK (difficulty_rating BETWEEN 1 AND 5),
    soreness_level TEXT NOT NULL,
    user_comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 12. Conversations & Messages
CREATE TABLE IF NOT EXISTS public.conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT 'New Conversation',
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE IF NOT EXISTS public.messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    sender_role sender_role_enum NOT NULL,
    content TEXT NOT NULL,
    citations JSONB DEFAULT '[]'::jsonb,
    structured_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 13. Reports Table
CREATE TABLE IF NOT EXISTS public.reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    summary_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    ai_summary TEXT,
    pdf_url TEXT,
    generated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 14. AI Usage Log Table
CREATE TABLE IF NOT EXISTS public.ai_usage_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    request_type TEXT NOT NULL,
    model_name TEXT NOT NULL,
    prompt_tokens INT NOT NULL DEFAULT 0,
    completion_tokens INT NOT NULL DEFAULT 0,
    latency_ms INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
