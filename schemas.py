from pydantic import BaseModel, Field
from typing import List, Optional


class Citation(BaseModel):
    document_id: str
    clause_id: str


class RAGResponse(BaseModel):
    answer: str
    citations: List[Citation]
    applicable_policy: Optional[str] = None
    step_sequence: List[str] = Field(default_factory=list)
    responsible_role: Optional[str] = None
    confidence: str
    abstained: bool