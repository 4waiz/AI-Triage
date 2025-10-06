from pydantic import BaseModel, Field
from typing import List, Optional

class AssessRequest(BaseModel):
    symptoms_text: str = Field(..., description="Arabic or English free-text symptoms")
    language: str = Field("ar", description="user language code, e.g., 'ar' or 'en'")

class TriageJSON(BaseModel):
    chief_complaint: str
    urgency_level: str  # emergent | urgent | non-urgent
    disposition: str    # ED | Outpatient | Self-care
    red_flags: List[str]
    required_specialty: Optional[str] = None
    reasoning: str
    instructions_ar: Optional[str] = None
    triage_score: int = 0  # 0–100
    confidence: float = 0.0 # 0–1

class AccessDecision(BaseModel):
    recommendation: str  # ED | Outpatient
    instructions_en: Optional[str] = None

class AssessResponse(BaseModel):
    recommendation: str
    severity: str
    red_flags: List[str]
    specialty: Optional[str]
    reasoning: str
    instructions: str
    next_step_url: str
