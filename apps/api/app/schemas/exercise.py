from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class ExerciseMediaResponse(BaseModel):
    id: UUID
    media_type: str
    url: str
    thumbnail_url: Optional[str] = None
    license_type: str
    attribution_text: str

class ExerciseResponse(BaseModel):
    id: UUID
    slug: str
    name: str
    category: str
    difficulty: str
    primary_muscles: List[str] = Field(default_factory=list)
    secondary_muscles: List[str] = Field(default_factory=list)
    equipment_needed: List[str] = Field(default_factory=list)
    suitable_age_groups: List[str] = Field(default_factory=list)
    instructions: str
    tips: Optional[str] = None
    contraindications: Optional[str] = None
    media: List[ExerciseMediaResponse] = Field(default_factory=list)
    created_at: Optional[datetime] = None

class ExerciseListResponse(BaseModel):
    data: List[ExerciseResponse]
    page: int
    page_size: int
    total_records: int
    total_pages: int
