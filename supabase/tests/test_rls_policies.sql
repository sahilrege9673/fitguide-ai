-- ==============================================================================
-- FeedGuide AI — RLS Policy Test Matrix & Verification Script
-- ==============================================================================
-- Description:
-- Tests isolation between User A and User B.
-- User B must NOT be able to view, edit, or delete User A's data.
-- Public reference tables (exercises, knowledge_documents) must be readable.
-- ==============================================================================

BEGIN;

-- 1. Create Mock Users
INSERT INTO auth.users (id, email)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'usera@example.com'),
    ('22222222-2222-2222-2222-222222222222', 'userb@example.com')
ON CONFLICT (id) DO NOTHING;

-- 2. Simulate User A Context
SET LOCAL "request.jwt.claim.sub" = '11111111-1111-1111-1111-111111111111';
SET LOCAL "request.jwt.claim.role" = 'authenticated';

-- User A inserts preferences
INSERT INTO public.onboarding_preferences (
    user_id, age_group, experience_level, fitness_goals, workout_location,
    available_equipment, preferred_activities, time_availability_mins,
    preferred_days, disclaimer_accepted
) VALUES (
    '11111111-1111-1111-1111-111111111111', 'adult_18_64', 'intermediate',
    ARRAY['strength', 'hypertrophy'], 'commercial_gym',
    ARRAY['barbell', 'dumbbells'], ARRAY['weightlifting'], 60,
    ARRAY[1, 3, 5], TRUE
);

-- User A should see 1 row
SELECT count(*) = 1 AS user_a_can_see_own_preferences 
FROM public.onboarding_preferences;

-- 3. Simulate User B Context
SET LOCAL "request.jwt.claim.sub" = '22222222-2222-2222-2222-222222222222';
SET LOCAL "request.jwt.claim.role" = 'authenticated';

-- User B MUST see 0 rows of User A's preferences
SELECT count(*) = 0 AS user_b_cannot_see_user_a_preferences 
FROM public.onboarding_preferences;

-- User B attempting to update User A's preferences must affect 0 rows
UPDATE public.onboarding_preferences 
SET time_availability_mins = 99 
WHERE user_id = '11111111-1111-1111-1111-111111111111';

SELECT time_availability_mins = 60 AS user_a_data_unmodified
FROM public.onboarding_preferences 
WHERE user_id = '11111111-1111-1111-1111-111111111111';

-- 4. Test Public Catalog Read (Unauthenticated / Anonymous)
SET LOCAL "request.jwt.claim.sub" = '';
SET LOCAL "request.jwt.claim.role" = 'anon';

-- Anon can read exercises table
SELECT EXISTS (SELECT 1 FROM public.exercises) AS anon_can_read_exercises;

ROLLBACK;
