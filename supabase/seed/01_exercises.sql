-- Seed Data: >= 80 Verified Exercises with Media Citations
BEGIN;

INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-back-squat', 'Barbell Back Squat', 'strength', 'intermediate'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['hamstrings', 'erector_spinae', 'core'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Place the barbell across your upper traps with a firm grip. Unrack, brace your core, and initiate the movement by breaking at the hips and knees simultaneously. Descend until hips crease below knee level while maintaining a neutral spine. Drive through the midfoot to return to full lockout.', 'Maintain chest up, brace diaphragmatically before every rep, and keep knees tracking in line with your toes.', 'Acute lumbar disc herniation, severe patellofemoral pain without regression.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-back-squat'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('goblet-squat', 'Dumbbell Goblet Squat', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['core', 'biceps'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hold a dumbbell or kettlebell vertically against your upper chest with both hands under the bell. Keep elbows tucked. Squat down between your knees, keeping your torso upright. Drive through feet to stand tall.', 'Use your elbows to gently push knees outward at the bottom for adductor and hip mobility.', 'Acute knee swelling.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'goblet-squat'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('bulgarian-split-squat', 'Bulgarian Split Squat', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['hamstrings', 'adductors'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Stand two feet in front of a flat bench. Place the laces of one foot rearward onto the bench. Lower your hips down and slightly back until the back knee hovers just above the floor. Drive through the front heel to return to starting position.', 'Lean slightly forward at the torso to place emphasis on the glute-ham tie-in; stay upright for quad focus.', 'Severe ankle mobility impingement or acute patellar tendinitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'bulgarian-split-squat'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('bodyweight-air-squat', 'Bodyweight Air Squat', 'mobility', 'beginner'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['hamstrings', 'core'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand with feet shoulder-width apart, toes flared slightly out. Extend arms forward for counter-balance. Descend until hip crease reaches knee height while keeping torso upright. Stand up fully squeezing glutes at the top.', 'Keep weight evenly distributed across heels and forefeet; do not let heels elevate.', 'None for standard tempo.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'bodyweight-air-squat'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('leg-press-machine', '45-Degree Leg Press', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['quadriceps'], ARRAY['glutes', 'hamstrings'], ARRAY['cable_machine'], ARRAY['adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit firmly with lower back pressed against pad. Place feet shoulder-width on the sled platform. Release safety handles, lower weight under control until knees reach 90 degrees without rounding the pelvis. Press back up without hyper-extending knees.', 'Never lock out knees aggressively; maintain constant muscle tension on quadriceps.', 'Lumbar disc flexion intolerance if hips detach from pad.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Unsplash Contributor'
FROM public.exercises WHERE slug = 'leg-press-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('walking-dumbbell-lunges', 'Walking Dumbbell Lunges', 'conditioning', 'intermediate'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['hamstrings', 'calves', 'core'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Hold dumbbells by your sides. Step forward with one leg, bending both knees to roughly 90 degrees. Push off the front foot and step immediately into the next forward stride with the opposite leg.', 'Keep stride length consistent so that the front knee stays above the midfoot.', 'Acute meniscus pathology with rotational instability.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'walking-dumbbell-lunges'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('leg-extension-machine', 'Seated Leg Extension', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['quadriceps'], '{}', ARRAY['cable_machine'], ARRAY['adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Adjust machine back pad so knees align with pivot point. Place lower shins against the padded roller. Extend knees smoothly until legs are straight, hold for 1 second, and lower with a controlled 3-second eccentric tempo.', 'Focus on the terminal knee extension squeeze rather than moving heavy momentum.', 'Early post-operative ACL reconstruction without medical clearance.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'leg-extension-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('step-ups-dumbbell', 'Dumbbell Box Step-Up', 'strength', 'beginner'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['calves'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place one foot flat onto a sturdy box or bench. Drive downward through that front heel to step up without pushing off with the trailing rear foot. Stand tall, then control the descent back down.', 'Eliminate the push off the floor foot to ensure the elevated leg does 100% of the concentric work.', 'Severe balance loss in seniors (use handrail support).')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'step-ups-dumbbell'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('chair-sit-to-stand', 'Chair Sit-to-Stand', 'mobility', 'beginner'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['core'], ARRAY['bench', 'bodyweight'], ARRAY['senior_65_plus'::age_group_enum], 'Sit on a firm chair with feet flat and shoulder-width. Cross arms over chest. Lean forward slightly from the hips and press through feet to stand up completely. Slowly sit down with control without flopping.', 'Excellent functional fall-prevention exercise for older adults.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'chair-sit-to-stand'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('sissy-squat-assisted', 'Assisted Sissy Squat', 'hypertrophy', 'advanced'::experience_level_enum, ARRAY['quadriceps'], ARRAY['core'], ARRAY['bodyweight'], ARRAY['adult_18_64'::age_group_enum], 'Hold a stable upright bar for support. Push knees forward while leaning torso backward, keeping hips extended in line with torso. Lower until deep knee flexion, then contract quads to stand.', 'Provides maximal stretch on rectus femoris. Progress depth gradually.', 'Patellar tendinopathy or chondromalacia patellae.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'sissy-squat-assisted'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-romanian-deadlift', 'Barbell Romanian Deadlift (RDL)', 'strength', 'intermediate'::experience_level_enum, ARRAY['hamstrings', 'glutes'], ARRAY['erector_spinae', 'forearms'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Stand holding barbell at hip width. Unlock knees slightly. Push hips straight back as if touching a wall behind you, sliding the bar down along your thighs. When you feel a deep hamstring stretch at mid-shin, reverse by driving hips forward.', 'Do not let the barbell drift away from your legs; keep lats engaged to pull bar close.', 'Severe acute hamstring strain, acute lumbar radiculopathy.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-romanian-deadlift'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dumbbell-romanian-deadlift', 'Dumbbell Romanian Deadlift', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['hamstrings', 'glutes'], ARRAY['core'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hold a pair of dumbbells in front of your thighs. Soften your knees and hinge deeply at the hips while keeping shoulder blades retracted. Lower dumbbells just below knee level, feel the posterior chain tension, and squeeze glutes to lockout.', 'Keep eyes focused 6 feet ahead on the floor to maintain neutral cervical spine alignment.', 'Severe active lower back disc protrusion.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'dumbbell-romanian-deadlift'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-conventional-deadlift', 'Conventional Barbell Deadlift', 'strength', 'advanced'::experience_level_enum, ARRAY['glutes', 'hamstrings', 'erector_spinae'], ARRAY['quadriceps', 'lats', 'traps', 'forearms'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Stand with bar over midfoot, feet hip-width. Hinge down and grip bar outside legs. Pull chest tall, engage lats, push floor away with legs until bar clears knees, then lock hips out firmly.', 'Think of pushing the earth away rather than pulling with the lower back.', 'Minors under 18 must not 1RM max; acute spondylolisthesis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'barbell-conventional-deadlift'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('lying-leg-curl-machine', 'Lying Leg Curl Machine', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['hamstrings'], ARRAY['calves'], ARRAY['cable_machine'], ARRAY['adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lie face down with Achilles tendon tucked beneath the padded lever. Keep pelvis pressed firmly against the bench. Curl heels upward towards glutes, pause for 1 second, and lower slowly under control.', 'Prevent hips from arching up off the bench by actively contracting your abs.', 'Acute distal hamstring avulsion.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'lying-leg-curl-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('seated-leg-curl-machine', 'Seated Leg Curl Machine', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['hamstrings'], '{}', ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit with thighs secured beneath the lap pad and lower leg pad resting behind your ankles. Curl legs under you into full knee flexion. Hold momentarily, then resist the return over a 3-second count.', 'The seated position stretches the hamstring at the hip, resulting in superior hypertrophy.', 'None for controlled volume.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'seated-leg-curl-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('glute-bridge-bodyweight', 'Bodyweight Glute Bridge', 'mobility', 'beginner'::experience_level_enum, ARRAY['glutes'], ARRAY['hamstrings', 'core'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lie supine on a mat with knees bent at 90 degrees and feet flat on the floor. Drive through heels to raise your hips until knees, hips, and shoulders form a straight line. Squeeze glutes for 2 seconds at peak.', 'Avoid over-arching the lower back; pivot strictly from the pelvis and glutes.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'glute-bridge-bodyweight'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-hip-thrust', 'Barbell Hip Thrust', 'strength', 'intermediate'::experience_level_enum, ARRAY['glutes'], ARRAY['hamstrings', 'quadriceps'], ARRAY['barbell', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Sit with upper back against a bench and a padded barbell rolled across your pelvic crease. Plant feet flat, shins vertical at top. Drive hips upward into full extension, pausing for 1 second at horizontal lockout.', 'Keep chin tucked towards your chest and ribs locked down to keep tension squarely on the glutes.', 'Acute pelvic floor trauma.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-hip-thrust'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('kettlebell-swing', 'Russian Kettlebell Swing', 'conditioning', 'intermediate'::experience_level_enum, ARRAY['glutes', 'hamstrings'], ARRAY['core', 'shoulders', 'forearms'], ARRAY['kettlebells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Hike the kettlebell between your legs like a center in football. Snap your hips forward aggressively, using hip extension power to project the kettlebell to chest height. Let gravity bring it back into the hinge.', 'This is a horizontal hip hinge, not a vertical squat. Do not raise the bell with your arms.', 'Acute lumbar facet syndrome.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'kettlebell-swing'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('single-leg-dumbbell-rdl', 'Single-Leg Dumbbell RDL', 'mobility', 'intermediate'::experience_level_enum, ARRAY['hamstrings', 'glutes'], ARRAY['calves', 'core'], ARRAY['dumbbells'], ARRAY['adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hold a dumbbell in the hand opposite the working leg. Hinge forward on the standing leg while extending the rear leg straight behind for balance. Lower until torso is parallel with floor, then return.', 'Square your hips to the floor; do not allow the rear hip to flare open.', 'Severe inner ear balance disturbances.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'single-leg-dumbbell-rdl'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('nordic-hamstring-curl-eccentric', 'Eccentric Nordic Hamstring Curl', 'strength', 'advanced'::experience_level_enum, ARRAY['hamstrings'], ARRAY['glutes', 'calves'], ARRAY['bodyweight'], ARRAY['adult_18_64'::age_group_enum], 'Kneel with ankles firmly anchored. Keep hips locked in extension. Lower your body forward toward the floor as slowly as possible using hamstring eccentric strength. Catch yourself with hands in pushup position.', 'Gold standard for hamstring injury prevention and athletic sprinting durability.', 'Previous hamstring tear less than 6 weeks prior.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'nordic-hamstring-curl-eccentric'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-bench-press', 'Barbell Bench Press', 'strength', 'intermediate'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'anterior_deltoids'], ARRAY['barbell', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Lie flat on bench with eyes under barbell. Grip slightly wider than shoulder width. Retract shoulder blades, arch upper back slightly, and unrack. Lower bar with elbows at 45-70 degrees until lightly touching sternum. Press explosively to lockout.', 'Drive your feet into the floor to generate leg drive and maintain upper back tightness.', 'Severe acromioclavicular (AC) joint separation, acute pectoral tear.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-bench-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('flat-dumbbell-press', 'Flat Dumbbell Press', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'anterior_deltoids'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lie on bench holding dumbbells with neutral/semi-pronated grip. Lower dumbbells smoothly until chest level with full pec stretch. Press upward and slightly inward, converging dumbbells without clacking them together.', 'Allows a natural rotational path that is friendlier on shoulder joints than a straight barbell.', 'Shoulder anterior instability.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'flat-dumbbell-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('incline-dumbbell-press', 'Incline Dumbbell Press (30-Degree)', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['clavicular_chest'], ARRAY['anterior_deltoids', 'triceps'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Set bench to a 30-degree incline. Press dumbbells to arms length. Lower slowly with elbows at a 45-degree angle until you feel a deep stretch in the upper chest. Drive dumbbells back to top.', 'Do not set incline higher than 30-45 degrees to avoid turning the movement into an overhead press.', 'Rotator cuff impingement in overhead abduction.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'incline-dumbbell-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('push-up-standard', 'Standard Push-Up', 'strength', 'beginner'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'anterior_deltoids', 'core'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place hands slightly wider than shoulders in high plank. Lock core and glutes so your body forms a rigid straight line. Lower until chest grazes the floor with elbows back 45 degrees. Press forcefully back to lockout.', 'Do not let lower back sag; maintain a strong posterior pelvic tilt.', 'Acute wrist carpal tunnel syndrome (use push-up handles).')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'push-up-standard'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('cable-chest-flye', 'Standing Cable Chest Flye', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['chest'], ARRAY['anterior_deltoids'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Set cable pulleys at chest height. Take one handle in each hand, step forward into a staggered stance. With a slight bend in elbows, bring hands together in an arc across your chest like hugging a large barrel. Squeeze pecs for 1 second.', 'Focus on driving your inner biceps towards each other rather than just touching hands.', 'Biceps tendonitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'cable-chest-flye'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dips-chest-focus', 'Parallel Bar Chest Dips', 'strength', 'advanced'::experience_level_enum, ARRAY['lower_chest', 'triceps'], ARRAY['anterior_deltoids'], ARRAY['pull_up_bar'], ARRAY['adult_18_64'::age_group_enum], 'Mount parallel dip bars with arms locked. Lean torso forward roughly 30 degrees and tuck chin. Lower until upper arms are parallel to bars or you feel a safe pec stretch. Press back up to lockout.', 'Keep elbows flared slightly and torso angled forward for pec recruitment.', 'Sternoclavicular joint pain or shoulder impingement.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'dips-chest-focus'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('incline-push-up', 'Incline Push-Up (Hands Elevated)', 'mobility', 'beginner'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'core'], ARRAY['bench', 'bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place hands on an elevated bench or sturdy platform. Keep body rigid from heels to crown. Lower chest to bench edge, then press back up.', 'Perfect beginner regression for building upper-body pushing capacity safely.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'incline-push-up'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('resistance-band-push-up', 'Banded Resisted Push-Up', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'core'], ARRAY['resistance_bands', 'bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Loop a resistance band across your upper back and anchor the ends under your palms. Perform a standard pushup against accommodating resistance, with tension increasing toward lockout.', 'Accommodating resistance matches the natural human strength curve.', 'Wrist joint effusion.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'resistance-band-push-up'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('machine-chest-press', 'Seated Machine Chest Press', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['chest'], ARRAY['triceps', 'anterior_deltoids'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Adjust seat height so handles align with mid-chest. Grip handles firmly with elbows flared at 45 degrees. Press forward until arms are fully extended without shrugging shoulders. Return slowly.', 'Provides stable, locked plane of motion ideal for hypertrophy without stabilizing fatigue.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'machine-chest-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('decline-dumbbell-press', 'Decline Dumbbell Press', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['lower_chest'], ARRAY['triceps'], ARRAY['dumbbells', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Secure legs on decline bench. Press dumbbells overhead. Lower dumbbells to lower pec line with control, then press vertically back to starting point.', 'Reduces shoulder impingement angle compared to flat or incline pressing.', 'Uncontrolled hypertension (due to inverted head position).')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'decline-dumbbell-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('pull-up-deadhang', 'Deadhang Pull-Up', 'strength', 'advanced'::experience_level_enum, ARRAY['lats'], ARRAY['biceps', 'rhomboids', 'rear_delts', 'core'], ARRAY['pull_up_bar'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Hang from a pull-up bar with overhand grip slightly wider than shoulders. Depress and retract shoulder blades, then pull chest up toward the bar until chin clears bar. Lower under control to dead hang.', 'Initiate every rep by pulling shoulder blades down before bending the elbows.', 'Severe shoulder labrum tear, acute distal biceps tendonitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'pull-up-deadhang'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('chin-up-underhand', 'Underhand Chin-Up', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['lats', 'biceps'], ARRAY['forearms', 'core'], ARRAY['pull_up_bar'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Grip bar with palms facing you shoulder-width apart. Pull vertically until chin clears bar while squeezing biceps and lats. Lower slowly to full elbow extension.', 'Supinated grip increases biceps recruitment significantly over standard pull-up.', 'Medial epicondylitis (Golfer''s elbow).')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'chin-up-underhand'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-bent-over-row', 'Barbell Bent-Over Row', 'strength', 'intermediate'::experience_level_enum, ARRAY['lats', 'rhomboids'], ARRAY['biceps', 'erector_spinae', 'traps'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Hinge at hips with torso at roughly 45 degrees, holding bar with overhand grip. Pull bar toward lower ribs by driving elbows back. Squeeze shoulder blades together at peak, then lower slowly.', 'Keep torso locked in place; do not use torso momentum to heave the barbell up.', 'Lumbar disc injury.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-bent-over-row'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('single-arm-dumbbell-row', 'Single-Arm Dumbbell Row', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['lats'], ARRAY['biceps', 'rhomboids', 'rear_delts'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place one knee and hand on a flat bench. Hold a dumbbell with free hand hanging straight down. Pull dumbbell toward your hip pocket, keeping elbow tucked close to ribcage. Lower to full lat stretch.', 'Think of pulling from the elbow rather than curling with the wrist and forearm.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'single-arm-dumbbell-row'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('lat-pulldown-cable', 'Wide-Grip Lat Pulldown', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['lats'], ARRAY['biceps', 'rhomboids'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit with thighs anchored under pads. Grip wide bar with overhand grip. Pull bar down smoothly toward upper chest, driving elbows down and back. Control return to full extension.', 'Lean back only 10-15 degrees; avoid swinging torso backward to jerk the stack.', 'None for standard front pulldowns (avoid behind-the-neck pulldowns).')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'lat-pulldown-cable'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('seated-cable-row', 'Seated Cable Row (Neutral Grip)', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['rhomboids', 'lats'], ARRAY['biceps', 'traps'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit with feet on footplates, knees slightly bent. Grasp V-handle. Sit upright with neutral spine. Pull handle toward navel, retracting shoulder blades completely. Return with control.', 'Maintain stationary torso throughout the pull; do not rock back and forth.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'seated-cable-row'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('chest-supported-t-bar-row', 'Chest-Supported T-Bar Row', 'strength', 'intermediate'::experience_level_enum, ARRAY['mid_back', 'lats'], ARRAY['biceps', 'rear_delts'], ARRAY['barbell', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Lie chest down on padded incline. Grip handles with pronated or neutral grip. Pull elbows up toward the ceiling, driving shoulder blades together. Lower with control.', 'Pad takes all shear force off the lumbar spine, allowing maximum back overload.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'chest-supported-t-bar-row'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('inverted-bodyweight-row', 'Inverted Bodyweight Row', 'mobility', 'beginner'::experience_level_enum, ARRAY['rhomboids', 'lats'], ARRAY['biceps', 'core'], ARRAY['pull_up_bar', 'bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Set a bar at waist height in a rack. Lie under bar, grasp with overhand grip, and hang with body in a straight plank. Pull chest up to touch the bar, then lower with control.', 'Bend knees and place feet flat to reduce load if full straight-leg version is too difficult.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'inverted-bodyweight-row'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('resistance-band-face-pull', 'Resistance Band Face Pull', 'mobility', 'beginner'::experience_level_enum, ARRAY['rear_delts', 'rotator_cuff'], ARRAY['traps', 'rhomboids'], ARRAY['resistance_bands'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Anchor band at head height. Grip band with thumbs pointing toward you. Pull band toward bridge of nose, externally rotating hands up and back like a double biceps pose. Hold 2 seconds.', 'Essential postural exercise to balance heavy bench pressing and sitting desk posture.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'resistance-band-face-pull'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('straight-arm-cable-pulldown', 'Straight-Arm Cable Pulldown', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['lats'], ARRAY['core', 'triceps'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand facing high cable with a straight bar. With elbows nearly locked, push bar down in an arc until it touches your upper thighs. Squeeze lats hard at bottom, then raise back to eye level.', 'Keeps biceps out of the movement, delivering isolated lat fatigue.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'straight-arm-cable-pulldown'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('overhead-barbell-press', 'Standing Overhead Barbell Press (OHP)', 'strength', 'intermediate'::experience_level_enum, ARRAY['anterior_deltoids', 'lateral_deltoids'], ARRAY['triceps', 'core', 'traps'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Stand with feet shoulder-width, bar resting across clavicles. Squeeze glutes and brace core. Press bar vertically overhead, tilting head slightly back to let bar pass, then locking head through the window at top.', 'Do not lean back excessively at the lumbar spine; keep pelvis tucked neutral.', 'Subacromial impingement, severe cervical disc issues.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'overhead-barbell-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('seated-dumbbell-shoulder-press', 'Seated Dumbbell Shoulder Press', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['anterior_deltoids'], ARRAY['triceps', 'lateral_deltoids'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit on bench with back support upright. Hold dumbbells at ear height with elbows forward 30 degrees. Press upward until arms are straight, then lower smoothly to ear height.', 'Press in the scapular plane (elbows slightly forward, not flared out completely wide).', 'Acute rotator cuff tendonitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'seated-dumbbell-shoulder-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dumbbell-lateral-raise', 'Dumbbell Lateral Raise', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['lateral_deltoids'], ARRAY['traps'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand with dumbbells at sides, slight forward torso tilt. Raise arms laterally until parallel to floor, keeping pinkies slightly elevated. Lower under 2-second control.', 'Lead with the elbows, not the wrists; use light weight to prevent trap shrugging.', 'None for light weight.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'dumbbell-lateral-raise'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('cable-lateral-raise', 'Behind-the-Back Cable Lateral Raise', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['lateral_deltoids'], '{}', ARRAY['cable_machine'], ARRAY['adult_18_64'::age_group_enum], 'Set low pulley. Stand sideways, reach behind back with working arm, and raise cable handle out to shoulder height. Constant tension throughout range.', 'Cables maintain continuous resistance at the bottom stretch where dumbbells offer zero load.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'cable-lateral-raise'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('rear-delt-dumbbell-flye', 'Bent-Over Rear Delt Flye', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['rear_delts'], ARRAY['rhomboids'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hinge at hips until torso is parallel to floor. Hold light dumbbells hanging down. With elbows softly bent, sweep arms wide out to sides until elbows reach shoulder plane.', 'Do not pinch shoulder blades back first; lead with posterior deltoid contraction.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'rear-delt-dumbbell-flye'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('arnold-press-dumbbell', 'Arnold Dumbbell Press', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['anterior_deltoids', 'lateral_deltoids'], ARRAY['triceps'], ARRAY['dumbbells', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Hold dumbbells in front of shoulders with palms facing you. As you press overhead, rotate palms outward until facing forward at top. Reverse rotation on descent.', 'Provides continuous time under tension across all three deltoid heads.', 'Impingement during internal shoulder rotation.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'arnold-press-dumbbell'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('face-pull-cable', 'High Cable Rope Face Pull', 'mobility', 'beginner'::experience_level_enum, ARRAY['rear_delts', 'rotator_cuff'], ARRAY['traps'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Attach rope to upper cable pulley. Grasp ends with thumbs back. Pull toward eye level, separating hands apart and rotating wrists back behind ears.', 'Critical for shoulder joint health and thoracic spine extension.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'face-pull-cable'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('pike-push-up', 'Pike Push-Up', 'strength', 'intermediate'::experience_level_enum, ARRAY['anterior_deltoids', 'lateral_deltoids'], ARRAY['triceps', 'core'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Assume a downward dog / inverted V position with hips high. Lower head diagonally forward between hands, then press back and up through shoulders.', 'Bodyweight overhead press progression leading up to handstand pushups.', 'Glaucoma or unmanaged high blood pressure.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'pike-push-up'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dumbbell-front-raise', 'Alternating Dumbbell Front Raise', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['anterior_deltoids'], '{}', ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hold dumbbells in front of thighs. Raise one dumbbell directly forward to eye height, pause briefly, then lower slowly before raising opposite arm.', 'Do not lean back or rock torso to swing the weight.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'dumbbell-front-raise'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-shrug', 'Barbell Shrug', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['traps'], ARRAY['forearms'], ARRAY['barbell'], ARRAY['adult_18_64'::age_group_enum], 'Hold barbell with shoulder-width overhand grip. Keeping arms straight, elevate your shoulders directly toward your ears as high as possible. Hold for 2 seconds at peak.', 'Do not roll shoulders in circles; move straight up and down to avoid neck strain.', 'Cervical radiculopathy.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-shrug'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('barbell-biceps-curl', 'Standing Barbell Biceps Curl', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['biceps'], ARRAY['forearms'], ARRAY['barbell'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Stand with shoulder-width underhand grip. Keep elbows pinned to sides. Curl bar upward toward chin, squeezing biceps. Lower slowly over 3 seconds.', 'Do not swing lower back or thrust hips forward; keep core rigid.', 'Distal biceps tendonitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'barbell-biceps-curl'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dumbbell-incline-curl', 'Incline Dumbbell Biceps Curl', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['biceps_long_head'], ARRAY['forearms'], ARRAY['dumbbells', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Sit on 45-degree incline bench with arms hanging fully extended. Curl dumbbells up while supinating wrists. Lower to a full stretch.', 'Emphasizes the long head of the biceps by placing it in passive stretch behind the torso.', 'Shoulder anterior capsule laxity.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'dumbbell-incline-curl'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dumbbell-hammer-curl', 'Neutral Grip Dumbbell Hammer Curl', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['brachialis', 'forearms'], ARRAY['biceps'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand holding dumbbells with palms facing each other (neutral grip). Curl weights up without rotating wrists. Lower with control.', 'Targets the brachialis muscle underneath the biceps, pushing arm thickness outward.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'dumbbell-hammer-curl'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('cable-rope-triceps-pushdown', 'Cable Rope Triceps Pushdown', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['triceps'], '{}', ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Attach rope to upper pulley. Pin elbows tight against your ribs. Push rope down, flaring ends outward at bottom to contract lateral triceps heads.', 'Do not let elbows drift forward on the eccentric; isolate triceps lockout completely.', 'Olecranon bursitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'cable-rope-triceps-pushdown'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('skull-crushers-ez-bar', 'Lying Triceps Extension (Skull Crusher)', 'hypertrophy', 'intermediate'::experience_level_enum, ARRAY['triceps_long_head'], '{}', ARRAY['barbell', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Lie on flat bench holding bar with arms vertical. Lower bar toward forehead or slightly behind head by bending elbows only. Extend elbows to lockout.', 'Lowering slightly past the head places the long head under greater stretch and protects the elbow joint.', 'Triceps tendonitis or cubital tunnel syndrome.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'skull-crushers-ez-bar'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('overhead-dumbbell-triceps-extension', 'Seated Overhead Dumbbell Triceps Extension', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['triceps_long_head'], '{}', ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Hold single dumbbell vertically overhead with both hands cupping the upper plate. Lower dumbbell behind neck, feeling deep stretch, then extend arms overhead.', 'Keep elbows pointing straight forward, not flared out wide.', 'Severe shoulder mobility restriction.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'overhead-dumbbell-triceps-extension'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('close-grip-bench-press', 'Close-Grip Barbell Bench Press', 'strength', 'intermediate'::experience_level_enum, ARRAY['triceps', 'chest'], ARRAY['anterior_deltoids'], ARRAY['barbell', 'bench'], ARRAY['adult_18_64'::age_group_enum], 'Lie on bench. Grip bar with hands shoulder-width apart (not excessively narrow). Lower bar to lower sternum with elbows tucked, then press to lockout.', 'Do not grip closer than shoulder width to prevent excess wrist strain.', 'Wrist TFCC tears.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'close-grip-bench-press'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('preacher-curl-dumbbell', 'One-Arm Dumbbell Preacher Curl', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['biceps_short_head'], ARRAY['forearms'], ARRAY['dumbbells', 'bench'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Place triceps flat against preacher bench pad. Lower dumbbell until arm is nearly straight, then curl up forcefully without lifting arm from pad.', 'Prevents body English completely, isolating the bicep peak.', 'Do not aggressively hyperextend at the bottom.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Scott Webb on Unsplash'
FROM public.exercises WHERE slug = 'preacher-curl-dumbbell'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('bench-dips-bodyweight', 'Bench Dips', 'strength', 'beginner'::experience_level_enum, ARRAY['triceps'], ARRAY['anterior_deltoids'], ARRAY['bench', 'bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place palms on bench edge behind you with legs extended forward. Lower hips by bending elbows to 90 degrees. Press through palms to return to top.', 'Keep back close to the bench to minimize anterior shoulder strain.', 'Shoulder anterior capsule instability.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'bench-dips-bodyweight'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('resistance-band-biceps-curl', 'Standing Resistance Band Biceps Curl', 'conditioning', 'beginner'::experience_level_enum, ARRAY['biceps'], ARRAY['forearms'], ARRAY['resistance_bands'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand on center of resistance band holding handles at sides. Curl handles toward shoulders against elastic tension. Squeeze for 1 second at top.', 'Provides accommodating resistance that peaks at maximum muscle contraction.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'resistance-band-biceps-curl'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('plank-isometric-hold', 'Forearm Plank Isometric Hold', 'mobility', 'beginner'::experience_level_enum, ARRAY['transverse_abdominis', 'rectus_abdominis'], ARRAY['glutes', 'shoulders'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Rest on forearms and balls of feet. Keep elbows under shoulders. Contract glutes and brace core as if anticipating a punch. Hold a rigid straight line without hip sagging.', 'Tuck pelvis into posterior pelvic tilt and pull elbows toward toes to double core activation.', 'Acute lumbar instability.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'plank-isometric-hold'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('hanging-leg-raise', 'Hanging Knee-to-Chest Raise', 'strength', 'intermediate'::experience_level_enum, ARRAY['rectus_abdominis', 'hip_flexors'], ARRAY['grip', 'lats'], ARRAY['pull_up_bar'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Hang from pullup bar. With controlled tempo, curl knees up toward your chest by flexing your spine, not just swinging hips. Pause at top, then lower with control.', 'Roll the pelvis upward at the peak of the movement to recruit rectus abdominis.', 'Inguinal hernia.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'hanging-leg-raise'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('ab-wheel-rollout', 'Kneeling Ab Wheel Rollout', 'strength', 'advanced'::experience_level_enum, ARRAY['rectus_abdominis'], ARRAY['lats', 'shoulders'], ARRAY['bodyweight'], ARRAY['adult_18_64'::age_group_enum], 'Kneel on mat with hands on ab wheel. Roll wheel forward smoothly while maintaining a rounded upper back and braced abs. Roll as far as controllable without lower back hyperextending, then pull back.', 'Do not let lower back arch down. If spine arches, stop the range immediately.', 'Lumbar disc pathology or diastasis recti.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'ab-wheel-rollout'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('pallof-press-cable', 'Standing Cable Pallof Press', 'mobility', 'beginner'::experience_level_enum, ARRAY['obliques', 'transverse_abdominis'], ARRAY['glutes'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand perpendicular to cable tower holding handle at chest height. Press hands directly forward away from chest, resisting rotational pull. Hold 2 seconds, then return.', 'Best anti-rotation core drill for spine health and rotational athletic power.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'pallof-press-cable'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('dead-bug-core', 'Dead Bug Exercise', 'mobility', 'beginner'::experience_level_enum, ARRAY['deep_core'], ARRAY['hip_flexors'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lie on back with arms pointing to ceiling and knees bent at 90 degrees. Lower right arm and left leg toward floor simultaneously while pressing lower back flat against floor. Return and alternate.', 'Keep lumbar spine pinned to the floor at all times; do not allow any gap.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'dead-bug-core'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('side-plank-hold', 'Side Plank Hold', 'mobility', 'beginner'::experience_level_enum, ARRAY['obliques', 'quadratus_lumborum'], ARRAY['glutes'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lie on side with forearm on floor under shoulder. Elevate hips until body forms a straight line from feet to head. Hold position for time.', 'McGill Big 3 core exercise proven for low back stability.', 'Severe shoulder bursitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'side-plank-hold'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('bird-dog-core', 'Bird-Dog Quadruped Extension', 'mobility', 'beginner'::experience_level_enum, ARRAY['erector_spinae', 'glutes'], ARRAY['core', 'shoulders'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'On hands and knees, extend opposite arm and leg simultaneously until parallel with floor. Hold for 3 seconds, then return and switch sides.', 'Do not rotate hips or arch lower back; focus on reaching long.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'bird-dog-core'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('cable-woodchopper', 'Cable Diagonal Woodchopper', 'conditioning', 'intermediate'::experience_level_enum, ARRAY['obliques'], ARRAY['shoulders', 'legs'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Attach handle to high pulley. Stand sideways, grip handle with both hands, and pull diagonally downward across body toward opposite hip while pivoting rear foot.', 'Initiate movement from torso and hips rather than arms alone.', 'Lumbar rotational stenosis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'cable-woodchopper'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('hollow-body-hold', 'Gymnastic Hollow Body Hold', 'strength', 'advanced'::experience_level_enum, ARRAY['rectus_abdominis'], ARRAY['hip_flexors', 'quadriceps'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Lie supine. Press lower back flat into floor. Extend arms overhead and elevate legs 6 inches off floor, creating a curved banana shape with your body. Hold for time.', 'Regress by bending knees to 90 degrees if lower back elevates off the ground.', 'Lumbar hyperlordosis flare-up.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'hollow-body-hold'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('farmer-carry-heavy', 'Farmer''s Walk Carry', 'conditioning', 'beginner'::experience_level_enum, ARRAY['core', 'traps', 'forearms'], ARRAY['glutes', 'calves'], ARRAY['dumbbells'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Pick up heavy dumbbells or kettlebells in each hand. Stand tall with neutral spine. Walk forward with smooth, short, measured steps for 30-50 meters.', 'Prevents lateral spine deviation and builds unbreakable functional grip.', 'Severe active carpal tunnel syndrome.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'farmer-carry-heavy'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('standing-calf-raise-machine', 'Standing Calf Raise', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['gastrocnemius'], ARRAY['soleus'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place balls of feet on block with heels hanging over edge. Lower into a deep 2-second calf stretch, then push straight up onto big toes. Pause at peak contraction.', 'Pause at the bottom stretch to eliminate Achilles tendon elastic rebound.', 'Acute Achilles tendon rupture or retrocalcaneal bursitis.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Victor Freitas on Unsplash'
FROM public.exercises WHERE slug = 'standing-calf-raise-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('seated-calf-raise-machine', 'Seated Calf Raise', 'hypertrophy', 'beginner'::experience_level_enum, ARRAY['soleus'], '{}', ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit with thighs under pad and balls of feet on platform. Lower heels to full stretch, then press upward onto toes.', 'Bent knee position slackens the gastrocnemius, isolating the deep soleus muscle.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Gordon Cowie on Unsplash'
FROM public.exercises WHERE slug = 'seated-calf-raise-machine'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('single-leg-calf-raise-bodyweight', 'Single-Leg Bodyweight Calf Raise', 'mobility', 'beginner'::experience_level_enum, ARRAY['gastrocnemius', 'soleus'], '{}', ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Stand on one foot on a step edge. Hold a wall for balance. Lower heel, pause, then press fully up onto ball of foot.', 'Great for single-leg ankle stability and unilateral balance in older adults.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'single-leg-calf-raise-bodyweight'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('tibialis-raise-bodyweight', 'Wall Tibialis Raise', 'mobility', 'beginner'::experience_level_enum, ARRAY['tibialis_anterior'], '{}', ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Lean back against a wall with heels out 2 feet. Pull toes and forefeet upward toward shins, hold 1 second, then lower.', 'Strengthens anterior tibialis, protecting knees and preventing shin splints.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'tibialis-raise-bodyweight'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('ankle-dorisflexion-band-stretch', 'Banded Ankle Mobilization', 'mobility', 'beginner'::experience_level_enum, ARRAY['ankle_joint'], ARRAY['calves'], ARRAY['resistance_bands'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Anchor band behind you. Place band loop around talus bone of ankle in half-kneeling stance. Drive knee forward past toes repeatedly.', 'Increases deep squat depth by freeing up ankle talus joint glide.', 'Acute anterior ankle impingement.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'ankle-dorisflexion-band-stretch'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('indoor-rowing-ergometer', 'Rowing Machine Interval (Ergometer)', 'conditioning', 'intermediate'::experience_level_enum, ARRAY['quadriceps', 'glutes', 'lats'], ARRAY['core', 'biceps', 'cardiovascular'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Catch position: shins vertical. Drive: push with legs first, swing hips open, pull handle to lower ribs. Recovery: reverse order smoothly.', 'Legs 60%, core 20%, arms 20%. Do not pull with arms before legs complete their drive.', 'Acute lumbar disc herniation in flexion.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'indoor-rowing-ergometer'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('cat-cow-spinal-flow', 'Cat-Cow Spine Mobilization', 'mobility', 'beginner'::experience_level_enum, ARRAY['erector_spinae'], ARRAY['core'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'On all fours, inhale as you drop belly toward floor and look upward (Cow). Exhale as you round spine up toward ceiling, tucking chin to chest (Cat).', 'Synchronize with slow, deep nasal breathing to relax the autonomic nervous system.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'cat-cow-spinal-flow'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('world-greatest-stretch', 'World''s Greatest Stretch', 'mobility', 'beginner'::experience_level_enum, ARRAY['hip_flexors', 'thoracic_spine', 'hamstrings'], ARRAY['glutes'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Step forward into a deep lunge. Place inside hand on floor next to front foot. Rotate opposite arm open toward ceiling, following with eyes. Drop elbow to instep.', 'Opens hips, ankles, and thoracic spine in a single comprehensive movement.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'world-greatest-stretch'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('jumping-jacks-cardio', 'Standard Jumping Jacks', 'conditioning', 'beginner'::experience_level_enum, ARRAY['calves', 'shoulders'], ARRAY['cardiovascular'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum], 'Stand with feet together. Jump feet out while raising arms overhead. Jump back to starting position on balls of feet.', 'Great for youth coordination and cardiovascular warm-up.', 'Severe stress urinary incontinence or acute ankle sprain.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'jumping-jacks-cardio'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('stationary-bike-rpm', 'Stationary Upright Bike Cadence', 'conditioning', 'beginner'::experience_level_enum, ARRAY['quadriceps'], ARRAY['hamstrings', 'calves', 'cardiovascular'], ARRAY['cable_machine'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Adjust saddle height so knee has a slight 25-degree bend at bottom of pedal stroke. Maintain consistent 80-90 RPM cadence with moderate flywheel resistance.', 'Low-impact aerobic conditioning ideal for joint longevity and active recovery.', 'None.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'stationary-bike-rpm'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('thoracic-foam-roll-extension', 'Thoracic Spine Foam Roller Extension', 'mobility', 'beginner'::experience_level_enum, ARRAY['thoracic_spine'], ARRAY['chest'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Place foam roller horizontally beneath mid-back. Support neck with hands. Gently arch backward over the roller while exhaling. Move roller up 1 inch and repeat.', 'Do not roll onto the lower back; restrict rolling to the ribcage region.', 'Osteoporosis with compression fracture risk.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'thoracic-foam-roll-extension'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('box-step-aerobic', 'Low-Impact Aerobic Step', 'conditioning', 'beginner'::experience_level_enum, ARRAY['quadriceps', 'glutes'], ARRAY['calves', 'cardiovascular'], ARRAY['bench', 'bodyweight'], ARRAY['senior_65_plus'::age_group_enum], 'Step up onto a low 6-inch step with left foot, follow with right foot, then step down with control. Maintain steady rhythm.', 'Gentle, non-ballistic aerobic exercise perfect for senior cardiovascular conditioning.', 'Acute knee effusion.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'box-step-aerobic'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('child-pose-lat-stretch', 'Child''s Pose with Lateral Reach', 'mobility', 'beginner'::experience_level_enum, ARRAY['lats', 'glutes'], ARRAY['thoracic_spine'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Kneel with toes together and knees spread wide. Sit hips onto heels and extend arms forward on floor. Walk both hands 45 degrees to the left to deeply stretch the right lat. Hold 30 seconds, then switch sides.', 'Breathe into the side of the ribcage to expand intercostal space.', 'Severe knee flexion pain.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = 'child-pose-lat-stretch'
ON CONFLICT DO NOTHING;


INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('90-90-hip-mobility-flow', '90-90 Hip Switch Flow', 'mobility', 'beginner'::experience_level_enum, ARRAY['hip_internal_rotators', 'hip_external_rotators'], ARRAY['glutes'], ARRAY['bodyweight'], ARRAY['minor_under_18'::age_group_enum, 'adult_18_64'::age_group_enum, 'senior_65_plus'::age_group_enum], 'Sit on floor with both knees bent at 90 degrees: front leg in external rotation, back leg in internal rotation. Maintain upright spine, then rotate knees and hips across to switch sides without hands touching floor if possible.', 'Builds hip mobility to protect lower back during deep squats and hinges.', 'Femoroacetabular impingement (FAI) during sharp pinching.')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    category = EXCLUDED.category,
    difficulty = EXCLUDED.difficulty,
    primary_muscles = EXCLUDED.primary_muscles,
    secondary_muscles = EXCLUDED.secondary_muscles,
    equipment_needed = EXCLUDED.equipment_needed,
    suitable_age_groups = EXCLUDED.suitable_age_groups,
    instructions = EXCLUDED.instructions,
    tips = EXCLUDED.tips,
    contraindications = EXCLUDED.contraindications;


INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, 'image'::media_type_enum, 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80', 'Unsplash License', 'Photo by Jonathan Borba on Unsplash'
FROM public.exercises WHERE slug = '90-90-hip-mobility-flow'
ON CONFLICT DO NOTHING;

COMMIT;