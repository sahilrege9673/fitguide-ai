from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str

class ErrorPayload(BaseModel):
    code: str
    message: str
    details: List[ErrorDetail] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorEnvelope(BaseModel):
    error: ErrorPayload

class PaginationMetadata(BaseModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int
