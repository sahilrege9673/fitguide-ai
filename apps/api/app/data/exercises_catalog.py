"""
FitGuide AI — Authoritative Exercise Reference Catalog (>= 80 Verified Exercises)
Includes biomechanical execution instructions, contraindications, age suitability, and media licensing attribution.
"""

from typing import List, Dict, Any

EXERCISES_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. QUADRICEPS & LOWER BODY COMPOUND (1-10)
    # -------------------------------------------------------------------------
    {
        "slug": "barbell-back-squat",
        "name": "Barbell Back Squat",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "erector_spinae", "core"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Place the barbell across your upper traps with a firm grip. Unrack, brace your core, and initiate the movement by breaking at the hips and knees simultaneously. Descend until hips crease below knee level while maintaining a neutral spine. Drive through the midfoot to return to full lockout.",
        "tips": "Maintain chest up, brace diaphragmatically before every rep, and keep knees tracking in line with your toes.",
        "contraindications": "Acute lumbar disc herniation, severe patellofemoral pain without regression.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "goblet-squat",
        "name": "Dumbbell Goblet Squat",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["core", "biceps"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Hold a dumbbell or kettlebell vertically against your upper chest with both hands under the bell. Keep elbows tucked. Squat down between your knees, keeping your torso upright. Drive through feet to stand tall.",
        "tips": "Use your elbows to gently push knees outward at the bottom for adductor and hip mobility.",
        "contraindications": "Acute knee swelling.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "bulgarian-split-squat",
        "name": "Bulgarian Split Squat",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "adductors"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Stand two feet in front of a flat bench. Place the laces of one foot rearward onto the bench. Lower your hips down and slightly back until the back knee hovers just above the floor. Drive through the front heel to return to starting position.",
        "tips": "Lean slightly forward at the torso to place emphasis on the glute-ham tie-in; stay upright for quad focus.",
        "contraindications": "Severe ankle mobility impingement or acute patellar tendinitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "bodyweight-air-squat",
        "name": "Bodyweight Air Squat",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand with feet shoulder-width apart, toes flared slightly out. Extend arms forward for counter-balance. Descend until hip crease reaches knee height while keeping torso upright. Stand up fully squeezing glutes at the top.",
        "tips": "Keep weight evenly distributed across heels and forefeet; do not let heels elevate.",
        "contraindications": "None for standard tempo.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "leg-press-machine",
        "name": "45-Degree Leg Press",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": ["glutes", "hamstrings"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["adult_18_64", "senior_65_plus"],
        "instructions": "Sit firmly with lower back pressed against pad. Place feet shoulder-width on the sled platform. Release safety handles, lower weight under control until knees reach 90 degrees without rounding the pelvis. Press back up without hyper-extending knees.",
        "tips": "Never lock out knees aggressively; maintain constant muscle tension on quadriceps.",
        "contraindications": "Lumbar disc flexion intolerance if hips detach from pad.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Unsplash Contributor"
            }
        ]
    },
    {
        "slug": "walking-dumbbell-lunges",
        "name": "Walking Dumbbell Lunges",
        "category": "conditioning",
        "difficulty": "intermediate",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["hamstrings", "calves", "core"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Hold dumbbells by your sides. Step forward with one leg, bending both knees to roughly 90 degrees. Push off the front foot and step immediately into the next forward stride with the opposite leg.",
        "tips": "Keep stride length consistent so that the front knee stays above the midfoot.",
        "contraindications": "Acute meniscus pathology with rotational instability.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "leg-extension-machine",
        "name": "Seated Leg Extension",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": [],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["adult_18_64", "senior_65_plus"],
        "instructions": "Adjust machine back pad so knees align with pivot point. Place lower shins against the padded roller. Extend knees smoothly until legs are straight, hold for 1 second, and lower with a controlled 3-second eccentric tempo.",
        "tips": "Focus on the terminal knee extension squeeze rather than moving heavy momentum.",
        "contraindications": "Early post-operative ACL reconstruction without medical clearance.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "step-ups-dumbbell",
        "name": "Dumbbell Box Step-Up",
        "category": "strength",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["calves"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place one foot flat onto a sturdy box or bench. Drive downward through that front heel to step up without pushing off with the trailing rear foot. Stand tall, then control the descent back down.",
        "tips": "Eliminate the push off the floor foot to ensure the elevated leg does 100% of the concentric work.",
        "contraindications": "Severe balance loss in seniors (use handrail support).",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "chair-sit-to-stand",
        "name": "Chair Sit-to-Stand",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["core"],
        "equipment_needed": ["bench", "bodyweight"],
        "suitable_age_groups": ["senior_65_plus"],
        "instructions": "Sit on a firm chair with feet flat and shoulder-width. Cross arms over chest. Lean forward slightly from the hips and press through feet to stand up completely. Slowly sit down with control without flopping.",
        "tips": "Excellent functional fall-prevention exercise for older adults.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "sissy-squat-assisted",
        "name": "Assisted Sissy Squat",
        "category": "hypertrophy",
        "difficulty": "advanced",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": ["core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Hold a stable upright bar for support. Push knees forward while leaning torso backward, keeping hips extended in line with torso. Lower until deep knee flexion, then contract quads to stand.",
        "tips": "Provides maximal stretch on rectus femoris. Progress depth gradually.",
        "contraindications": "Patellar tendinopathy or chondromalacia patellae.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 2. POSTERIOR CHAIN & HAMSTRINGS (11-20)
    # -------------------------------------------------------------------------
    {
        "slug": "barbell-romanian-deadlift",
        "name": "Barbell Romanian Deadlift (RDL)",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["hamstrings", "glutes"],
        "secondary_muscles": ["erector_spinae", "forearms"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Stand holding barbell at hip width. Unlock knees slightly. Push hips straight back as if touching a wall behind you, sliding the bar down along your thighs. When you feel a deep hamstring stretch at mid-shin, reverse by driving hips forward.",
        "tips": "Do not let the barbell drift away from your legs; keep lats engaged to pull bar close.",
        "contraindications": "Severe acute hamstring strain, acute lumbar radiculopathy.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "dumbbell-romanian-deadlift",
        "name": "Dumbbell Romanian Deadlift",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["hamstrings", "glutes"],
        "secondary_muscles": ["core"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Hold a pair of dumbbells in front of your thighs. Soften your knees and hinge deeply at the hips while keeping shoulder blades retracted. Lower dumbbells just below knee level, feel the posterior chain tension, and squeeze glutes to lockout.",
        "tips": "Keep eyes focused 6 feet ahead on the floor to maintain neutral cervical spine alignment.",
        "contraindications": "Severe active lower back disc protrusion.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "barbell-conventional-deadlift",
        "name": "Conventional Barbell Deadlift",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["glutes", "hamstrings", "erector_spinae"],
        "secondary_muscles": ["quadriceps", "lats", "traps", "forearms"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Stand with bar over midfoot, feet hip-width. Hinge down and grip bar outside legs. Pull chest tall, engage lats, push floor away with legs until bar clears knees, then lock hips out firmly.",
        "tips": "Think of pushing the earth away rather than pulling with the lower back.",
        "contraindications": "Minors under 18 must not 1RM max; acute spondylolisthesis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "lying-leg-curl-machine",
        "name": "Lying Leg Curl Machine",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["hamstrings"],
        "secondary_muscles": ["calves"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["adult_18_64", "senior_65_plus"],
        "instructions": "Lie face down with Achilles tendon tucked beneath the padded lever. Keep pelvis pressed firmly against the bench. Curl heels upward towards glutes, pause for 1 second, and lower slowly under control.",
        "tips": "Prevent hips from arching up off the bench by actively contracting your abs.",
        "contraindications": "Acute distal hamstring avulsion.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "seated-leg-curl-machine",
        "name": "Seated Leg Curl Machine",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["hamstrings"],
        "secondary_muscles": [],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit with thighs secured beneath the lap pad and lower leg pad resting behind your ankles. Curl legs under you into full knee flexion. Hold momentarily, then resist the return over a 3-second count.",
        "tips": "The seated position stretches the hamstring at the hip, resulting in superior hypertrophy.",
        "contraindications": "None for controlled volume.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "glute-bridge-bodyweight",
        "name": "Bodyweight Glute Bridge",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["glutes"],
        "secondary_muscles": ["hamstrings", "core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Lie supine on a mat with knees bent at 90 degrees and feet flat on the floor. Drive through heels to raise your hips until knees, hips, and shoulders form a straight line. Squeeze glutes for 2 seconds at peak.",
        "tips": "Avoid over-arching the lower back; pivot strictly from the pelvis and glutes.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "barbell-hip-thrust",
        "name": "Barbell Hip Thrust",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["glutes"],
        "secondary_muscles": ["hamstrings", "quadriceps"],
        "equipment_needed": ["barbell", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Sit with upper back against a bench and a padded barbell rolled across your pelvic crease. Plant feet flat, shins vertical at top. Drive hips upward into full extension, pausing for 1 second at horizontal lockout.",
        "tips": "Keep chin tucked towards your chest and ribs locked down to keep tension squarely on the glutes.",
        "contraindications": "Acute pelvic floor trauma.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "kettlebell-swing",
        "name": "Russian Kettlebell Swing",
        "category": "conditioning",
        "difficulty": "intermediate",
        "primary_muscles": ["glutes", "hamstrings"],
        "secondary_muscles": ["core", "shoulders", "forearms"],
        "equipment_needed": ["kettlebells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Hike the kettlebell between your legs like a center in football. Snap your hips forward aggressively, using hip extension power to project the kettlebell to chest height. Let gravity bring it back into the hinge.",
        "tips": "This is a horizontal hip hinge, not a vertical squat. Do not raise the bell with your arms.",
        "contraindications": "Acute lumbar facet syndrome.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "single-leg-dumbbell-rdl",
        "name": "Single-Leg Dumbbell RDL",
        "category": "mobility",
        "difficulty": "intermediate",
        "primary_muscles": ["hamstrings", "glutes"],
        "secondary_muscles": ["calves", "core"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["adult_18_64", "senior_65_plus"],
        "instructions": "Hold a dumbbell in the hand opposite the working leg. Hinge forward on the standing leg while extending the rear leg straight behind for balance. Lower until torso is parallel with floor, then return.",
        "tips": "Square your hips to the floor; do not allow the rear hip to flare open.",
        "contraindications": "Severe inner ear balance disturbances.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "nordic-hamstring-curl-eccentric",
        "name": "Eccentric Nordic Hamstring Curl",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["hamstrings"],
        "secondary_muscles": ["glutes", "calves"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Kneel with ankles firmly anchored. Keep hips locked in extension. Lower your body forward toward the floor as slowly as possible using hamstring eccentric strength. Catch yourself with hands in pushup position.",
        "tips": "Gold standard for hamstring injury prevention and athletic sprinting durability.",
        "contraindications": "Previous hamstring tear less than 6 weeks prior.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 3. CHEST & UPPER BODY PUSH (21-30)
    # -------------------------------------------------------------------------
    {
        "slug": "barbell-bench-press",
        "name": "Barbell Bench Press",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "anterior_deltoids"],
        "equipment_needed": ["barbell", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Lie flat on bench with eyes under barbell. Grip slightly wider than shoulder width. Retract shoulder blades, arch upper back slightly, and unrack. Lower bar with elbows at 45-70 degrees until lightly touching sternum. Press explosively to lockout.",
        "tips": "Drive your feet into the floor to generate leg drive and maintain upper back tightness.",
        "contraindications": "Severe acromioclavicular (AC) joint separation, acute pectoral tear.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "flat-dumbbell-press",
        "name": "Flat Dumbbell Press",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "anterior_deltoids"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Lie on bench holding dumbbells with neutral/semi-pronated grip. Lower dumbbells smoothly until chest level with full pec stretch. Press upward and slightly inward, converging dumbbells without clacking them together.",
        "tips": "Allows a natural rotational path that is friendlier on shoulder joints than a straight barbell.",
        "contraindications": "Shoulder anterior instability.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "incline-dumbbell-press",
        "name": "Incline Dumbbell Press (30-Degree)",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["clavicular_chest"],
        "secondary_muscles": ["anterior_deltoids", "triceps"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Set bench to a 30-degree incline. Press dumbbells to arms length. Lower slowly with elbows at a 45-degree angle until you feel a deep stretch in the upper chest. Drive dumbbells back to top.",
        "tips": "Do not set incline higher than 30-45 degrees to avoid turning the movement into an overhead press.",
        "contraindications": "Rotator cuff impingement in overhead abduction.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "push-up-standard",
        "name": "Standard Push-Up",
        "category": "strength",
        "difficulty": "beginner",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "anterior_deltoids", "core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place hands slightly wider than shoulders in high plank. Lock core and glutes so your body forms a rigid straight line. Lower until chest grazes the floor with elbows back 45 degrees. Press forcefully back to lockout.",
        "tips": "Do not let lower back sag; maintain a strong posterior pelvic tilt.",
        "contraindications": "Acute wrist carpal tunnel syndrome (use push-up handles).",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "cable-chest-flye",
        "name": "Standing Cable Chest Flye",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["anterior_deltoids"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Set cable pulleys at chest height. Take one handle in each hand, step forward into a staggered stance. With a slight bend in elbows, bring hands together in an arc across your chest like hugging a large barrel. Squeeze pecs for 1 second.",
        "tips": "Focus on driving your inner biceps towards each other rather than just touching hands.",
        "contraindications": "Biceps tendonitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "dips-chest-focus",
        "name": "Parallel Bar Chest Dips",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["lower_chest", "triceps"],
        "secondary_muscles": ["anterior_deltoids"],
        "equipment_needed": ["pull_up_bar"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Mount parallel dip bars with arms locked. Lean torso forward roughly 30 degrees and tuck chin. Lower until upper arms are parallel to bars or you feel a safe pec stretch. Press back up to lockout.",
        "tips": "Keep elbows flared slightly and torso angled forward for pec recruitment.",
        "contraindications": "Sternoclavicular joint pain or shoulder impingement.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "incline-push-up",
        "name": "Incline Push-Up (Hands Elevated)",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "core"],
        "equipment_needed": ["bench", "bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place hands on an elevated bench or sturdy platform. Keep body rigid from heels to crown. Lower chest to bench edge, then press back up.",
        "tips": "Perfect beginner regression for building upper-body pushing capacity safely.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "resistance-band-push-up",
        "name": "Banded Resisted Push-Up",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "core"],
        "equipment_needed": ["resistance_bands", "bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Loop a resistance band across your upper back and anchor the ends under your palms. Perform a standard pushup against accommodating resistance, with tension increasing toward lockout.",
        "tips": "Accommodating resistance matches the natural human strength curve.",
        "contraindications": "Wrist joint effusion.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "machine-chest-press",
        "name": "Seated Machine Chest Press",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["chest"],
        "secondary_muscles": ["triceps", "anterior_deltoids"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Adjust seat height so handles align with mid-chest. Grip handles firmly with elbows flared at 45 degrees. Press forward until arms are fully extended without shrugging shoulders. Return slowly.",
        "tips": "Provides stable, locked plane of motion ideal for hypertrophy without stabilizing fatigue.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "decline-dumbbell-press",
        "name": "Decline Dumbbell Press",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["lower_chest"],
        "secondary_muscles": ["triceps"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Secure legs on decline bench. Press dumbbells overhead. Lower dumbbells to lower pec line with control, then press vertically back to starting point.",
        "tips": "Reduces shoulder impingement angle compared to flat or incline pressing.",
        "contraindications": "Uncontrolled hypertension (due to inverted head position).",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 4. BACK & UPPER BODY PULL (31-40)
    # -------------------------------------------------------------------------
    {
        "slug": "pull-up-deadhang",
        "name": "Deadhang Pull-Up",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["biceps", "rhomboids", "rear_delts", "core"],
        "equipment_needed": ["pull_up_bar"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Hang from a pull-up bar with overhand grip slightly wider than shoulders. Depress and retract shoulder blades, then pull chest up toward the bar until chin clears bar. Lower under control to dead hang.",
        "tips": "Initiate every rep by pulling shoulder blades down before bending the elbows.",
        "contraindications": "Severe shoulder labrum tear, acute distal biceps tendonitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "chin-up-underhand",
        "name": "Underhand Chin-Up",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["lats", "biceps"],
        "secondary_muscles": ["forearms", "core"],
        "equipment_needed": ["pull_up_bar"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Grip bar with palms facing you shoulder-width apart. Pull vertically until chin clears bar while squeezing biceps and lats. Lower slowly to full elbow extension.",
        "tips": "Supinated grip increases biceps recruitment significantly over standard pull-up.",
        "contraindications": "Medial epicondylitis (Golfer's elbow).",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "barbell-bent-over-row",
        "name": "Barbell Bent-Over Row",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["lats", "rhomboids"],
        "secondary_muscles": ["biceps", "erector_spinae", "traps"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Hinge at hips with torso at roughly 45 degrees, holding bar with overhand grip. Pull bar toward lower ribs by driving elbows back. Squeeze shoulder blades together at peak, then lower slowly.",
        "tips": "Keep torso locked in place; do not use torso momentum to heave the barbell up.",
        "contraindications": "Lumbar disc injury.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "single-arm-dumbbell-row",
        "name": "Single-Arm Dumbbell Row",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["biceps", "rhomboids", "rear_delts"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place one knee and hand on a flat bench. Hold a dumbbell with free hand hanging straight down. Pull dumbbell toward your hip pocket, keeping elbow tucked close to ribcage. Lower to full lat stretch.",
        "tips": "Think of pulling from the elbow rather than curling with the wrist and forearm.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "lat-pulldown-cable",
        "name": "Wide-Grip Lat Pulldown",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["biceps", "rhomboids"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit with thighs anchored under pads. Grip wide bar with overhand grip. Pull bar down smoothly toward upper chest, driving elbows down and back. Control return to full extension.",
        "tips": "Lean back only 10-15 degrees; avoid swinging torso backward to jerk the stack.",
        "contraindications": "None for standard front pulldowns (avoid behind-the-neck pulldowns).",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "seated-cable-row",
        "name": "Seated Cable Row (Neutral Grip)",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["rhomboids", "lats"],
        "secondary_muscles": ["biceps", "traps"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit with feet on footplates, knees slightly bent. Grasp V-handle. Sit upright with neutral spine. Pull handle toward navel, retracting shoulder blades completely. Return with control.",
        "tips": "Maintain stationary torso throughout the pull; do not rock back and forth.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "chest-supported-t-bar-row",
        "name": "Chest-Supported T-Bar Row",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["mid_back", "lats"],
        "secondary_muscles": ["biceps", "rear_delts"],
        "equipment_needed": ["barbell", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Lie chest down on padded incline. Grip handles with pronated or neutral grip. Pull elbows up toward the ceiling, driving shoulder blades together. Lower with control.",
        "tips": "Pad takes all shear force off the lumbar spine, allowing maximum back overload.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "inverted-bodyweight-row",
        "name": "Inverted Bodyweight Row",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["rhomboids", "lats"],
        "secondary_muscles": ["biceps", "core"],
        "equipment_needed": ["pull_up_bar", "bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Set a bar at waist height in a rack. Lie under bar, grasp with overhand grip, and hang with body in a straight plank. Pull chest up to touch the bar, then lower with control.",
        "tips": "Bend knees and place feet flat to reduce load if full straight-leg version is too difficult.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "resistance-band-face-pull",
        "name": "Resistance Band Face Pull",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["rear_delts", "rotator_cuff"],
        "secondary_muscles": ["traps", "rhomboids"],
        "equipment_needed": ["resistance_bands"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Anchor band at head height. Grip band with thumbs pointing toward you. Pull band toward bridge of nose, externally rotating hands up and back like a double biceps pose. Hold 2 seconds.",
        "tips": "Essential postural exercise to balance heavy bench pressing and sitting desk posture.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "straight-arm-cable-pulldown",
        "name": "Straight-Arm Cable Pulldown",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["lats"],
        "secondary_muscles": ["core", "triceps"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand facing high cable with a straight bar. With elbows nearly locked, push bar down in an arc until it touches your upper thighs. Squeeze lats hard at bottom, then raise back to eye level.",
        "tips": "Keeps biceps out of the movement, delivering isolated lat fatigue.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 5. SHOULDERS & DELTOIDS (41-50)
    # -------------------------------------------------------------------------
    {
        "slug": "overhead-barbell-press",
        "name": "Standing Overhead Barbell Press (OHP)",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["anterior_deltoids", "lateral_deltoids"],
        "secondary_muscles": ["triceps", "core", "traps"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Stand with feet shoulder-width, bar resting across clavicles. Squeeze glutes and brace core. Press bar vertically overhead, tilting head slightly back to let bar pass, then locking head through the window at top.",
        "tips": "Do not lean back excessively at the lumbar spine; keep pelvis tucked neutral.",
        "contraindications": "Subacromial impingement, severe cervical disc issues.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "seated-dumbbell-shoulder-press",
        "name": "Seated Dumbbell Shoulder Press",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["anterior_deltoids"],
        "secondary_muscles": ["triceps", "lateral_deltoids"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit on bench with back support upright. Hold dumbbells at ear height with elbows forward 30 degrees. Press upward until arms are straight, then lower smoothly to ear height.",
        "tips": "Press in the scapular plane (elbows slightly forward, not flared out completely wide).",
        "contraindications": "Acute rotator cuff tendonitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "dumbbell-lateral-raise",
        "name": "Dumbbell Lateral Raise",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["lateral_deltoids"],
        "secondary_muscles": ["traps"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand with dumbbells at sides, slight forward torso tilt. Raise arms laterally until parallel to floor, keeping pinkies slightly elevated. Lower under 2-second control.",
        "tips": "Lead with the elbows, not the wrists; use light weight to prevent trap shrugging.",
        "contraindications": "None for light weight.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "cable-lateral-raise",
        "name": "Behind-the-Back Cable Lateral Raise",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["lateral_deltoids"],
        "secondary_muscles": [],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Set low pulley. Stand sideways, reach behind back with working arm, and raise cable handle out to shoulder height. Constant tension throughout range.",
        "tips": "Cables maintain continuous resistance at the bottom stretch where dumbbells offer zero load.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "rear-delt-dumbbell-flye",
        "name": "Bent-Over Rear Delt Flye",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["rear_delts"],
        "secondary_muscles": ["rhomboids"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Hinge at hips until torso is parallel to floor. Hold light dumbbells hanging down. With elbows softly bent, sweep arms wide out to sides until elbows reach shoulder plane.",
        "tips": "Do not pinch shoulder blades back first; lead with posterior deltoid contraction.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "arnold-press-dumbbell",
        "name": "Arnold Dumbbell Press",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["anterior_deltoids", "lateral_deltoids"],
        "secondary_muscles": ["triceps"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Hold dumbbells in front of shoulders with palms facing you. As you press overhead, rotate palms outward until facing forward at top. Reverse rotation on descent.",
        "tips": "Provides continuous time under tension across all three deltoid heads.",
        "contraindications": "Impingement during internal shoulder rotation.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "face-pull-cable",
        "name": "High Cable Rope Face Pull",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["rear_delts", "rotator_cuff"],
        "secondary_muscles": ["traps"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Attach rope to upper cable pulley. Grasp ends with thumbs back. Pull toward eye level, separating hands apart and rotating wrists back behind ears.",
        "tips": "Critical for shoulder joint health and thoracic spine extension.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "pike-push-up",
        "name": "Pike Push-Up",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["anterior_deltoids", "lateral_deltoids"],
        "secondary_muscles": ["triceps", "core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Assume a downward dog / inverted V position with hips high. Lower head diagonally forward between hands, then press back and up through shoulders.",
        "tips": "Bodyweight overhead press progression leading up to handstand pushups.",
        "contraindications": "Glaucoma or unmanaged high blood pressure.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "dumbbell-front-raise",
        "name": "Alternating Dumbbell Front Raise",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["anterior_deltoids"],
        "secondary_muscles": [],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Hold dumbbells in front of thighs. Raise one dumbbell directly forward to eye height, pause briefly, then lower slowly before raising opposite arm.",
        "tips": "Do not lean back or rock torso to swing the weight.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "barbell-shrug",
        "name": "Barbell Shrug",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["traps"],
        "secondary_muscles": ["forearms"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Hold barbell with shoulder-width overhand grip. Keeping arms straight, elevate your shoulders directly toward your ears as high as possible. Hold for 2 seconds at peak.",
        "tips": "Do not roll shoulders in circles; move straight up and down to avoid neck strain.",
        "contraindications": "Cervical radiculopathy.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 6. ARMS: BICEPS & TRICEPS (51-60)
    # -------------------------------------------------------------------------
    {
        "slug": "barbell-biceps-curl",
        "name": "Standing Barbell Biceps Curl",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["biceps"],
        "secondary_muscles": ["forearms"],
        "equipment_needed": ["barbell"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Stand with shoulder-width underhand grip. Keep elbows pinned to sides. Curl bar upward toward chin, squeezing biceps. Lower slowly over 3 seconds.",
        "tips": "Do not swing lower back or thrust hips forward; keep core rigid.",
        "contraindications": "Distal biceps tendonitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "dumbbell-incline-curl",
        "name": "Incline Dumbbell Biceps Curl",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["biceps_long_head"],
        "secondary_muscles": ["forearms"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Sit on 45-degree incline bench with arms hanging fully extended. Curl dumbbells up while supinating wrists. Lower to a full stretch.",
        "tips": "Emphasizes the long head of the biceps by placing it in passive stretch behind the torso.",
        "contraindications": "Shoulder anterior capsule laxity.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "dumbbell-hammer-curl",
        "name": "Neutral Grip Dumbbell Hammer Curl",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["brachialis", "forearms"],
        "secondary_muscles": ["biceps"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand holding dumbbells with palms facing each other (neutral grip). Curl weights up without rotating wrists. Lower with control.",
        "tips": "Targets the brachialis muscle underneath the biceps, pushing arm thickness outward.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "cable-rope-triceps-pushdown",
        "name": "Cable Rope Triceps Pushdown",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["triceps"],
        "secondary_muscles": [],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Attach rope to upper pulley. Pin elbows tight against your ribs. Push rope down, flaring ends outward at bottom to contract lateral triceps heads.",
        "tips": "Do not let elbows drift forward on the eccentric; isolate triceps lockout completely.",
        "contraindications": "Olecranon bursitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "skull-crushers-ez-bar",
        "name": "Lying Triceps Extension (Skull Crusher)",
        "category": "hypertrophy",
        "difficulty": "intermediate",
        "primary_muscles": ["triceps_long_head"],
        "secondary_muscles": [],
        "equipment_needed": ["barbell", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Lie on flat bench holding bar with arms vertical. Lower bar toward forehead or slightly behind head by bending elbows only. Extend elbows to lockout.",
        "tips": "Lowering slightly past the head places the long head under greater stretch and protects the elbow joint.",
        "contraindications": "Triceps tendonitis or cubital tunnel syndrome.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "overhead-dumbbell-triceps-extension",
        "name": "Seated Overhead Dumbbell Triceps Extension",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["triceps_long_head"],
        "secondary_muscles": [],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Hold single dumbbell vertically overhead with both hands cupping the upper plate. Lower dumbbell behind neck, feeling deep stretch, then extend arms overhead.",
        "tips": "Keep elbows pointing straight forward, not flared out wide.",
        "contraindications": "Severe shoulder mobility restriction.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "close-grip-bench-press",
        "name": "Close-Grip Barbell Bench Press",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["triceps", "chest"],
        "secondary_muscles": ["anterior_deltoids"],
        "equipment_needed": ["barbell", "bench"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Lie on bench. Grip bar with hands shoulder-width apart (not excessively narrow). Lower bar to lower sternum with elbows tucked, then press to lockout.",
        "tips": "Do not grip closer than shoulder width to prevent excess wrist strain.",
        "contraindications": "Wrist TFCC tears.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "preacher-curl-dumbbell",
        "name": "One-Arm Dumbbell Preacher Curl",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["biceps_short_head"],
        "secondary_muscles": ["forearms"],
        "equipment_needed": ["dumbbells", "bench"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Place triceps flat against preacher bench pad. Lower dumbbell until arm is nearly straight, then curl up forcefully without lifting arm from pad.",
        "tips": "Prevents body English completely, isolating the bicep peak.",
        "contraindications": "Do not aggressively hyperextend at the bottom.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1434608519344-49d77a699e1d?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Scott Webb on Unsplash"
            }
        ]
    },
    {
        "slug": "bench-dips-bodyweight",
        "name": "Bench Dips",
        "category": "strength",
        "difficulty": "beginner",
        "primary_muscles": ["triceps"],
        "secondary_muscles": ["anterior_deltoids"],
        "equipment_needed": ["bench", "bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place palms on bench edge behind you with legs extended forward. Lower hips by bending elbows to 90 degrees. Press through palms to return to top.",
        "tips": "Keep back close to the bench to minimize anterior shoulder strain.",
        "contraindications": "Shoulder anterior capsule instability.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "resistance-band-biceps-curl",
        "name": "Standing Resistance Band Biceps Curl",
        "category": "conditioning",
        "difficulty": "beginner",
        "primary_muscles": ["biceps"],
        "secondary_muscles": ["forearms"],
        "equipment_needed": ["resistance_bands"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand on center of resistance band holding handles at sides. Curl handles toward shoulders against elastic tension. Squeeze for 1 second at top.",
        "tips": "Provides accommodating resistance that peaks at maximum muscle contraction.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 7. CORE & ABDOMINALS (61-70)
    # -------------------------------------------------------------------------
    {
        "slug": "plank-isometric-hold",
        "name": "Forearm Plank Isometric Hold",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["transverse_abdominis", "rectus_abdominis"],
        "secondary_muscles": ["glutes", "shoulders"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Rest on forearms and balls of feet. Keep elbows under shoulders. Contract glutes and brace core as if anticipating a punch. Hold a rigid straight line without hip sagging.",
        "tips": "Tuck pelvis into posterior pelvic tilt and pull elbows toward toes to double core activation.",
        "contraindications": "Acute lumbar instability.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "hanging-leg-raise",
        "name": "Hanging Knee-to-Chest Raise",
        "category": "strength",
        "difficulty": "intermediate",
        "primary_muscles": ["rectus_abdominis", "hip_flexors"],
        "secondary_muscles": ["grip", "lats"],
        "equipment_needed": ["pull_up_bar"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Hang from pullup bar. With controlled tempo, curl knees up toward your chest by flexing your spine, not just swinging hips. Pause at top, then lower with control.",
        "tips": "Roll the pelvis upward at the peak of the movement to recruit rectus abdominis.",
        "contraindications": "Inguinal hernia.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "ab-wheel-rollout",
        "name": "Kneeling Ab Wheel Rollout",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["rectus_abdominis"],
        "secondary_muscles": ["lats", "shoulders"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["adult_18_64"],
        "instructions": "Kneel on mat with hands on ab wheel. Roll wheel forward smoothly while maintaining a rounded upper back and braced abs. Roll as far as controllable without lower back hyperextending, then pull back.",
        "tips": "Do not let lower back arch down. If spine arches, stop the range immediately.",
        "contraindications": "Lumbar disc pathology or diastasis recti.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "pallof-press-cable",
        "name": "Standing Cable Pallof Press",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["obliques", "transverse_abdominis"],
        "secondary_muscles": ["glutes"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand perpendicular to cable tower holding handle at chest height. Press hands directly forward away from chest, resisting rotational pull. Hold 2 seconds, then return.",
        "tips": "Best anti-rotation core drill for spine health and rotational athletic power.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "dead-bug-core",
        "name": "Dead Bug Exercise",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["deep_core"],
        "secondary_muscles": ["hip_flexors"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Lie on back with arms pointing to ceiling and knees bent at 90 degrees. Lower right arm and left leg toward floor simultaneously while pressing lower back flat against floor. Return and alternate.",
        "tips": "Keep lumbar spine pinned to the floor at all times; do not allow any gap.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "side-plank-hold",
        "name": "Side Plank Hold",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["obliques", "quadratus_lumborum"],
        "secondary_muscles": ["glutes"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Lie on side with forearm on floor under shoulder. Elevate hips until body forms a straight line from feet to head. Hold position for time.",
        "tips": "McGill Big 3 core exercise proven for low back stability.",
        "contraindications": "Severe shoulder bursitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "bird-dog-core",
        "name": "Bird-Dog Quadruped Extension",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["erector_spinae", "glutes"],
        "secondary_muscles": ["core", "shoulders"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "On hands and knees, extend opposite arm and leg simultaneously until parallel with floor. Hold for 3 seconds, then return and switch sides.",
        "tips": "Do not rotate hips or arch lower back; focus on reaching long.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "cable-woodchopper",
        "name": "Cable Diagonal Woodchopper",
        "category": "conditioning",
        "difficulty": "intermediate",
        "primary_muscles": ["obliques"],
        "secondary_muscles": ["shoulders", "legs"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Attach handle to high pulley. Stand sideways, grip handle with both hands, and pull diagonally downward across body toward opposite hip while pivoting rear foot.",
        "tips": "Initiate movement from torso and hips rather than arms alone.",
        "contraindications": "Lumbar rotational stenosis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "hollow-body-hold",
        "name": "Gymnastic Hollow Body Hold",
        "category": "strength",
        "difficulty": "advanced",
        "primary_muscles": ["rectus_abdominis"],
        "secondary_muscles": ["hip_flexors", "quadriceps"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Lie supine. Press lower back flat into floor. Extend arms overhead and elevate legs 6 inches off floor, creating a curved banana shape with your body. Hold for time.",
        "tips": "Regress by bending knees to 90 degrees if lower back elevates off the ground.",
        "contraindications": "Lumbar hyperlordosis flare-up.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "farmer-carry-heavy",
        "name": "Farmer's Walk Carry",
        "category": "conditioning",
        "difficulty": "beginner",
        "primary_muscles": ["core", "traps", "forearms"],
        "secondary_muscles": ["glutes", "calves"],
        "equipment_needed": ["dumbbells"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Pick up heavy dumbbells or kettlebells in each hand. Stand tall with neutral spine. Walk forward with smooth, short, measured steps for 30-50 meters.",
        "tips": "Prevents lateral spine deviation and builds unbreakable functional grip.",
        "contraindications": "Severe active carpal tunnel syndrome.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 8. CALVES & ANKLE MOBILITY (71-75)
    # -------------------------------------------------------------------------
    {
        "slug": "standing-calf-raise-machine",
        "name": "Standing Calf Raise",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["gastrocnemius"],
        "secondary_muscles": ["soleus"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place balls of feet on block with heels hanging over edge. Lower into a deep 2-second calf stretch, then push straight up onto big toes. Pause at peak contraction.",
        "tips": "Pause at the bottom stretch to eliminate Achilles tendon elastic rebound.",
        "contraindications": "Acute Achilles tendon rupture or retrocalcaneal bursitis.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Victor Freitas on Unsplash"
            }
        ]
    },
    {
        "slug": "seated-calf-raise-machine",
        "name": "Seated Calf Raise",
        "category": "hypertrophy",
        "difficulty": "beginner",
        "primary_muscles": ["soleus"],
        "secondary_muscles": [],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit with thighs under pad and balls of feet on platform. Lower heels to full stretch, then press upward onto toes.",
        "tips": "Bent knee position slackens the gastrocnemius, isolating the deep soleus muscle.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Gordon Cowie on Unsplash"
            }
        ]
    },
    {
        "slug": "single-leg-calf-raise-bodyweight",
        "name": "Single-Leg Bodyweight Calf Raise",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["gastrocnemius", "soleus"],
        "secondary_muscles": [],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Stand on one foot on a step edge. Hold a wall for balance. Lower heel, pause, then press fully up onto ball of foot.",
        "tips": "Great for single-leg ankle stability and unilateral balance in older adults.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "tibialis-raise-bodyweight",
        "name": "Wall Tibialis Raise",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["tibialis_anterior"],
        "secondary_muscles": [],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Lean back against a wall with heels out 2 feet. Pull toes and forefeet upward toward shins, hold 1 second, then lower.",
        "tips": "Strengthens anterior tibialis, protecting knees and preventing shin splints.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "ankle-dorisflexion-band-stretch",
        "name": "Banded Ankle Mobilization",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["ankle_joint"],
        "secondary_muscles": ["calves"],
        "equipment_needed": ["resistance_bands"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Anchor band behind you. Place band loop around talus bone of ankle in half-kneeling stance. Drive knee forward past toes repeatedly.",
        "tips": "Increases deep squat depth by freeing up ankle talus joint glide.",
        "contraindications": "Acute anterior ankle impingement.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # 9. AEROBIC, CONDITIONING & MOBILITY FLOWS (76-84)
    # -------------------------------------------------------------------------
    {
        "slug": "indoor-rowing-ergometer",
        "name": "Rowing Machine Interval (Ergometer)",
        "category": "conditioning",
        "difficulty": "intermediate",
        "primary_muscles": ["quadriceps", "glutes", "lats"],
        "secondary_muscles": ["core", "biceps", "cardiovascular"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Catch position: shins vertical. Drive: push with legs first, swing hips open, pull handle to lower ribs. Recovery: reverse order smoothly.",
        "tips": "Legs 60%, core 20%, arms 20%. Do not pull with arms before legs complete their drive.",
        "contraindications": "Acute lumbar disc herniation in flexion.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "cat-cow-spinal-flow",
        "name": "Cat-Cow Spine Mobilization",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["erector_spinae"],
        "secondary_muscles": ["core"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "On all fours, inhale as you drop belly toward floor and look upward (Cow). Exhale as you round spine up toward ceiling, tucking chin to chest (Cat).",
        "tips": "Synchronize with slow, deep nasal breathing to relax the autonomic nervous system.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "world-greatest-stretch",
        "name": "World's Greatest Stretch",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["hip_flexors", "thoracic_spine", "hamstrings"],
        "secondary_muscles": ["glutes"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Step forward into a deep lunge. Place inside hand on floor next to front foot. Rotate opposite arm open toward ceiling, following with eyes. Drop elbow to instep.",
        "tips": "Opens hips, ankles, and thoracic spine in a single comprehensive movement.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "jumping-jacks-cardio",
        "name": "Standard Jumping Jacks",
        "category": "conditioning",
        "difficulty": "beginner",
        "primary_muscles": ["calves", "shoulders"],
        "secondary_muscles": ["cardiovascular"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64"],
        "instructions": "Stand with feet together. Jump feet out while raising arms overhead. Jump back to starting position on balls of feet.",
        "tips": "Great for youth coordination and cardiovascular warm-up.",
        "contraindications": "Severe stress urinary incontinence or acute ankle sprain.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "stationary-bike-rpm",
        "name": "Stationary Upright Bike Cadence",
        "category": "conditioning",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps"],
        "secondary_muscles": ["hamstrings", "calves", "cardiovascular"],
        "equipment_needed": ["cable_machine"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Adjust saddle height so knee has a slight 25-degree bend at bottom of pedal stroke. Maintain consistent 80-90 RPM cadence with moderate flywheel resistance.",
        "tips": "Low-impact aerobic conditioning ideal for joint longevity and active recovery.",
        "contraindications": "None.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "thoracic-foam-roll-extension",
        "name": "Thoracic Spine Foam Roller Extension",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["thoracic_spine"],
        "secondary_muscles": ["chest"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Place foam roller horizontally beneath mid-back. Support neck with hands. Gently arch backward over the roller while exhaling. Move roller up 1 inch and repeat.",
        "tips": "Do not roll onto the lower back; restrict rolling to the ribcage region.",
        "contraindications": "Osteoporosis with compression fracture risk.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "box-step-aerobic",
        "name": "Low-Impact Aerobic Step",
        "category": "conditioning",
        "difficulty": "beginner",
        "primary_muscles": ["quadriceps", "glutes"],
        "secondary_muscles": ["calves", "cardiovascular"],
        "equipment_needed": ["bench", "bodyweight"],
        "suitable_age_groups": ["senior_65_plus"],
        "instructions": "Step up onto a low 6-inch step with left foot, follow with right foot, then step down with control. Maintain steady rhythm.",
        "tips": "Gentle, non-ballistic aerobic exercise perfect for senior cardiovascular conditioning.",
        "contraindications": "Acute knee effusion.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "child-pose-lat-stretch",
        "name": "Child's Pose with Lateral Reach",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["lats", "glutes"],
        "secondary_muscles": ["thoracic_spine"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Kneel with toes together and knees spread wide. Sit hips onto heels and extend arms forward on floor. Walk both hands 45 degrees to the left to deeply stretch the right lat. Hold 30 seconds, then switch sides.",
        "tips": "Breathe into the side of the ribcage to expand intercostal space.",
        "contraindications": "Severe knee flexion pain.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    },
    {
        "slug": "90-90-hip-mobility-flow",
        "name": "90-90 Hip Switch Flow",
        "category": "mobility",
        "difficulty": "beginner",
        "primary_muscles": ["hip_internal_rotators", "hip_external_rotators"],
        "secondary_muscles": ["glutes"],
        "equipment_needed": ["bodyweight"],
        "suitable_age_groups": ["minor_under_18", "adult_18_64", "senior_65_plus"],
        "instructions": "Sit on floor with both knees bent at 90 degrees: front leg in external rotation, back leg in internal rotation. Maintain upright spine, then rotate knees and hips across to switch sides without hands touching floor if possible.",
        "tips": "Builds hip mobility to protect lower back during deep squats and hinges.",
        "contraindications": "Femoroacetabular impingement (FAI) during sharp pinching.",
        "media": [
            {
                "media_type": "image",
                "url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80",
                "thumbnail_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=200&q=80",
                "license_type": "Unsplash License",
                "attribution_text": "Photo by Jonathan Borba on Unsplash"
            }
        ]
    }
]
