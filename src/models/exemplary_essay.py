from pydantic import BaseModel

class ExemplaryEssayRequest(BaseModel):
    theme: str

class ExemplaryEssayResponse(BaseModel):
    essay: str