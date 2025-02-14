from fastapi import HTTPException, Depends
from typing import Dict
from dotenv import load_dotenv
import uvicorn
import os

# Importe as funções necessárias do script original
from routes.evaluateEssay import grade_essay, ChatOpenAI, ChatPromptTemplate
from models.evaluateEssay import EssayRequest, EssayResponse, ImprovementRequest, ImprovementResponse
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
            "depth_score": result["depth_score"] * 10
        }
        logger.info(f"Avaliação concluída para usuário {current_user}")
        logger.debug(f"Detalhes da avaliação: {response}")
        return response
    except Exception as e:
        logger.error(f"Erro ao avaliar redação para usuário {current_user}: {str(e)}")
        logger.exception("Stacktrace completo:")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/suggest_improvements", response_model=ImprovementResponse)
async def api_suggest_improvements(request: ImprovementRequest, current_user: str = Depends(get_current_user)) -> Dict:
    logger.info(f"Requisição de sugestão de melhorias recebida de {current_user}")
    logger.debug(f"Tamanho da redação para análise: {len(request.essay)} caracteres")
    try:
        llm = ChatOpenAI(model="gpt-4o-mini")
        logger.debug("Modelo LLM inicializado")
        prompt = ChatPromptTemplate.from_template(
        """
            Você é um especialista em redação com mais de 20 anos de experiência na área e sua tarefa é analisar uma redação em português e fornecer sugestões de melhoria em termos de estrutura. 
            Leia atentamente o texto fornecido e avalie sua organização, gramática, coesão e coerência.

            Aqui está a redação a ser analisada:

            <redacao>
            {essay}
            </redacao>

            Analise cuidadosamente a estrutura da redação acima, considerando os seguintes elementos:

            1. Introdução: Presença de contextualização, tese e delimitação do tema
            2. Desenvolvimento: Organização dos parágrafos, uso de conectivos e progressão das ideias
            3. Conclusão: Retomada da tese, síntese dos argumentos e proposta de intervenção (se aplicável)
            4. Gramática: Correção gramatical e uso adequado da norma culta da língua
            5. Coesão: Uso adequado de elementos coesivos entre parágrafos e dentro deles
            6. Coerência: Manutenção do tema e da linha argumentativa ao longo do texto

            Com base na sua análise, forneça sugestões construtivas para melhorar a estrutura da redação. Concentre-se em como o autor pode reorganizar ou aprimorar o texto para torná-lo mais claro, coeso e coerente.

            Apresente sua análise e sugestões no seguinte formato:

            <analise>

            1. Pontos fortes da estrutura atual:
            [Liste os aspectos positivos da estrutura da redação]

            2. Áreas que necessitam de melhoria:
            [Identifique os elementos estruturais que podem ser aprimorados]

            3. Sugestões de melhoria:
            [Forneça sugestões específicas e práticas para melhorar a estrutura da redação]

            </analise>

            Lembre-se de ser construtivo e específico em suas sugestões, focando sempre na melhoria da estrutura do texto.
        """

        )
        result = llm.invoke(prompt.format(essay=request.essay))
        response = {"suggestions": result.content}
        logger.info(f"Sugestões geradas com sucesso para usuário {current_user}")
        logger.debug(f"Tamanho das sugestões: {len(response['suggestions'])} caracteres")
        return response
    except Exception as e:
        logger.error(f"Erro ao gerar sugestões para usuário {current_user}: {str(e)}")
        logger.exception("Stacktrace completo:")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

# Para executar use o seguinte comando:
# uvicorn nome_do_arquivo:app --reload