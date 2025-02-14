from fastapi import HTTPException, Depends, APIRouter
from typing import Dict
from routes.auth import get_current_user
from routes.agent_evaluate_essay import grade_essay
from models.evaluate_essay import EssayRequest, EssayResponse
from utils.logger import logger

router = APIRouter(tags=["Evaluate Essay"])

# Versão 1 da API
@router.post("/v1/grade_essay", response_model=EssayResponse)
async def api_grade_essay(request: EssayRequest, current_user: str = Depends(get_current_user)) -> Dict:
    logger.info(f"Requisição de avaliação de redação recebida de {current_user}")
    logger.debug(f"Tamanho da redação: {len(request.essay)} caracteres")
    try:
        result = grade_essay(request.essay)
        response = {
            "final_score": result["final_score"] * 10,
            "relevance_score": result["relevance_score"] * 10,
            "grammar_score": result["grammar_score"] * 10,
            "structure_score": result["structure_score"] * 10,
            "depth_score": result["depth_score"] * 10,
            "corrections": result["corrections"]
        }
        logger.info(f"Avaliação concluída para usuário {current_user}")
        logger.debug(f"Detalhes da avaliação: {response}")
        return response
    except Exception as e:
        logger.error(f"Erro ao avaliar redação para usuário {current_user}: {str(e)}")
        logger.exception("Stacktrace completo:")
        raise HTTPException(status_code=500, detail=str(e))