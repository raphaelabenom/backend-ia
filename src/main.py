from fastapi import HTTPException, Depends
from typing import Dict
from dotenv import load_dotenv
import uvicorn
import os

# Importe as funções necessárias do script original
from routes.evaluateEssay import grade_essay, ChatOpenAI, ChatPromptTemplate
from models.evaluateEssay import EssayRequest, EssayResponse, ExemplaryEssayRequest, ExemplaryEssayResponse
from extensions import app
from routes.auth import get_current_user
from utils.logger import logger

# Carregue as variáveis de ambiente
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Versão 1 da API
@app.post("/v1/grade_essay", response_model=EssayResponse)
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

@app.post("/v1/generate_exemplary_essay", response_model=ExemplaryEssayResponse)
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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

# Para executar use o seguinte comando:
# uvicorn main:app --reload