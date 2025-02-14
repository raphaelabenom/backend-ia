from pydantic import BaseModel

# Modelos Pydantic
class EssayRequest(BaseModel):
    essay: str

class EssayResponse(BaseModel):
    final_score: float
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float

class ImprovementRequest(BaseModel):
    essay: str

class ImprovementResponse(BaseModel):
    suggestions: str

class Token(BaseModel):
    access_token: str
    token_type: str