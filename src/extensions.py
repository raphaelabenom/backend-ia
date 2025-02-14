from fastapi import FastAPI

app = FastAPI(
    title="API de Avaliação de Redações",
    description="API para avaliação de redações e sugestão de melhorias usando Langgraph e OpenAI",
    version="1.0.0"
)
