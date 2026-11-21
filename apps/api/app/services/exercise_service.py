from typing import List, Optional, Dict, Any
from uuid import UUID, uuid5, NAMESPACE_DNS
from app.data.exercises_catalog import EXERCISES_DATA
from app.schemas.exercise import ExerciseResponse, ExerciseMediaResponse, ExerciseListResponse

class ExerciseService:
    _CATALOG_CACHE: Optional[List[ExerciseResponse]] = None

    @classmethod
    def _build_catalog(cls) -> List[ExerciseResponse]:
        if cls._CATALOG_CACHE is not None:
            return cls._CATALOG_CACHE

        exercises = []
        for raw in EXERCISES_DATA:
            ex_id = uuid5(NAMESPACE_DNS, f"feedguide.exercise.{raw['slug']}")
            media_items = []
            for idx, m in enumerate(raw.get("media", [])):
                m_id = uuid5(NAMESPACE_DNS, f"feedguide.media.{raw['slug']}.{idx}")
                media_items.append(ExerciseMediaResponse(
                    id=m_id,
                    media_type=m["media_type"],
                    url=m["url"],
                    thumbnail_url=m.get("thumbnail_url"),
                    license_type=m["license_type"],
                    attribution_text=m["attribution_text"]
                ))

            exercises.append(ExerciseResponse(
                id=ex_id,
                slug=raw["slug"],
                name=raw["name"],
                category=raw["category"],
                difficulty=raw["difficulty"],
                primary_muscles=raw.get("primary_muscles", []),
                secondary_muscles=raw.get("secondary_muscles", []),
                equipment_needed=raw.get("equipment_needed", []),
                suitable_age_groups=raw.get("suitable_age_groups", []),
                instructions=raw["instructions"],
                tips=raw.get("tips"),
                contraindications=raw.get("contraindications"),
                media=media_items
            ))

        cls._CATALOG_CACHE = exercises
        return exercises

    @classmethod
    def list_exercises(
        cls,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        muscle: Optional[str] = None,
        equipment: Optional[str] = None,
        age_group: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> ExerciseListResponse:
        catalog = cls._build_catalog()
        filtered = catalog

        if category:
            filtered = [e for e in filtered if e.category.lower() == category.lower()]
        if difficulty:
            filtered = [e for e in filtered if e.difficulty.lower() == difficulty.lower()]
        if muscle:
            m_clean = muscle.lower().replace("-", "_")
            filtered = [
                e for e in filtered 
                if any(m_clean in pm.lower() for pm in e.primary_muscles) 
                or any(m_clean in sm.lower() for sm in e.secondary_muscles)
            ]
        if equipment:
            eq_clean = equipment.lower().replace("-", "_")
            filtered = [e for e in filtered if any(eq_clean in eq.lower() for eq in e.equipment_needed)]
        if age_group:
            filtered = [e for e in filtered if age_group in e.suitable_age_groups]
        if search and search.strip():
            query = search.strip().lower()
            filtered = [
                e for e in filtered 
                if query in e.name.lower() 
                or query in e.instructions.lower() 
                or (e.tips and query in e.tips.lower())
                or query in e.slug.lower()
            ]

        total_records = len(filtered)
        total_pages = max(1, (total_records + page_size - 1) // page_size)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        return ExerciseListResponse(
            data=filtered[start_idx:end_idx],
            page=page,
            page_size=page_size,
            total_records=total_records,
            total_pages=total_pages
        )

    @classmethod
    def get_by_slug(cls, slug: str) -> Optional[ExerciseResponse]:
        catalog = cls._build_catalog()
        for e in catalog:
            if e.slug == slug:
                return e
        return None

    @classmethod
    def get_by_id(cls, exercise_id: UUID) -> Optional[ExerciseResponse]:
        catalog = cls._build_catalog()
        for e in catalog:
            if e.id == exercise_id:
                return e
        return None

    @classmethod
    def find_swap_alternative(
        cls,
        current_exercise: ExerciseResponse,
        user_age_group: str,
        user_equipment: List[str]
    ) -> Optional[ExerciseResponse]:
        """
        Finds a biologically and equipment-compatible alternative exercise
        targeting the same primary muscle group.
        """
        catalog = cls._build_catalog()
        # Find candidates sharing primary muscles, matching age group, not the same exercise
        candidates = []
        for e in catalog:
            if e.id == current_exercise.id:
                continue
            if user_age_group not in e.suitable_age_groups:
                continue
            # Must be compatible with user's equipment or bodyweight
            if e.equipment_needed and not any(eq in user_equipment or eq == "bodyweight" for eq in e.equipment_needed):
                continue
            
            # Match at least one primary muscle
            shared_muscles = set(current_exercise.primary_muscles).intersection(set(e.primary_muscles))
            if shared_muscles:
                candidates.append(e)

        if not candidates:
            # Fallback to category match
            candidates = [
                e for e in catalog 
                if e.category == current_exercise.category 
                and e.id != current_exercise.id 
                and user_age_group in e.suitable_age_groups
            ]

        return candidates[0] if candidates else None
