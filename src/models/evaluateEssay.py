from pydantic import BaseModel
from typing import TypedDict

# Modelos Pydantic
class State(TypedDict):
    """Representa o estado do processo de avaliação da redação."""
    essay: str
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    final_score: float
    corrections: str

class EssayRequest(BaseModel):
    essay: str

class EssayResponse(BaseModel):
    final_score: float
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    corrections: str

class ExemplaryEssayRequest(BaseModel):
    theme: str

class ExemplaryEssayResponse(BaseModel):
    essay: str

class Token(BaseModel):
    access_token: str
    token_type: str