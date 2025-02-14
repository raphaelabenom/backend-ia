from fastapi import HTTPException, Depends, APIRouter
from utils.logger import logger
from models.exemplary_essay import ExemplaryEssayRequest, ExemplaryEssayResponse
from routes.auth import get_current_user
from routes.agent_evaluate_essay import ChatOpenAI, ChatPromptTemplate

router = APIRouter(tags=["Generate Essay"])

# Versão 1 da API
@router.post("/v1/generate_exemplary_essay", response_model=ExemplaryEssayResponse)
async def api_generate_exemplary_essay(request: ExemplaryEssayRequest, current_user: str = Depends(get_current_user)) -> ExemplaryEssayResponse:
    logger.info(f"Requisição de geração de redação exemplar recebida de {current_user}")
    logger.debug(f"Tema da redação: {request.theme}")
    try:
        llm = ChatOpenAI(model="gpt-4o-mini")
        logger.debug("Modelo LLM inicializado")
        prompt = ChatPromptTemplate.from_template(
        """
            Você é um especialista em redação com mais de 20 anos de experiência na área e sua tarefa é gerar uma redação exemplar com base no tema fornecido.
            
            Tema da redação: {theme}
            
            Escreva uma redação de qualidade, seguindo as seguintes diretrizes:
            - Inclua uma introdução clara que apresenta o tema e estabelece a tese.
            - Desenvolva o tema com argumentos bem estruturados e coesos.
            - Conclua a redação com uma conclusão que retome a tese e faça uma síntese dos argumentos principais.
            - Use uma linguagem formal e clara.
            - Certifique-se de que a redação tenha uma boa organização e coesão.
            
            A redação deve ter cerca de 500 palavras.
        """
        )
        result = llm.invoke(prompt.format(theme=request.theme))
        response = ExemplaryEssayResponse(essay=result.content)
        logger.info(f"Redação exemplar gerada com sucesso para usuário {current_user}")
        logger.debug(f"Tamanho da redação: {len(response.essay)} caracteres")
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar redação exemplar para usuário {current_user}: {str(e)}")
        logger.exception("Stacktrace completo:")
        raise HTTPException(status_code=500, detail=str(e))