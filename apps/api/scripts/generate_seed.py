import sys
from pathlib import Path

# Add apps/api to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data.exercises_catalog import EXERCISES_DATA

sql = ['-- Seed Data: >= 80 Verified Exercises with Media Citations', 'BEGIN;']

for ex in EXERCISES_DATA:
    slug = ex['slug'].replace("'", "''")
    name = ex['name'].replace("'", "''")
    category = ex['category'].replace("'", "''")
    diff = ex['difficulty']
    prim = "ARRAY[" + ", ".join(f"'{m}'" for m in ex['primary_muscles']) + "]" if ex['primary_muscles'] else "'{}'"
    sec = "ARRAY[" + ", ".join(f"'{m}'" for m in ex['secondary_muscles']) + "]" if ex['secondary_muscles'] else "'{}'"
    equip = "ARRAY[" + ", ".join(f"'{e}'" for e in ex['equipment_needed']) + "]" if ex['equipment_needed'] else "'{}'"
    ages = "ARRAY[" + ", ".join(f"'{a}'::age_group_enum" for a in ex['suitable_age_groups']) + "]"
    inst = ex['instructions'].replace("'", "''")
    tips = ex.get('tips', '').replace("'", "''")
    contra = ex.get('contraindications', '').replace("'", "''")
    
    sql.append(f"""
INSERT INTO public.exercises (slug, name, category, difficulty, primary_muscles, secondary_muscles, equipment_needed, suitable_age_groups, instructions, tips, contraindications)
VALUES ('{slug}', '{name}', '{category}', '{diff}'::experience_level_enum, {prim}, {sec}, {equip}, {ages}, '{inst}', '{tips}', '{contra}')
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
""")
    for m in ex.get('media', []):
        m_type = m['media_type']
        url = m['url']
        thumb = m.get('thumbnail_url', '')
        lic = m['license_type'].replace("'", "''")
        attr = m['attribution_text'].replace("'", "''")
        sql.append(f"""
INSERT INTO public.exercise_media (exercise_id, media_type, url, thumbnail_url, license_type, attribution_text)
SELECT id, '{m_type}'::media_type_enum, '{url}', '{thumb}', '{lic}', '{attr}'
FROM public.exercises WHERE slug = '{slug}'
ON CONFLICT DO NOTHING;
""")

sql.append('COMMIT;')

seed_path = Path(__file__).parent.parent.parent.parent / 'supabase' / 'seed' / '01_exercises.sql'
seed_path.parent.mkdir(parents=True, exist_ok=True)
with open(seed_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql))

print(f'Successfully generated {seed_path} with {len(EXERCISES_DATA)} exercises.')
