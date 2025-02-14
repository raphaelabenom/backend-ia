from fastapi import FastAPI

app = FastAPI(
    title="API de Avaliação e geração de Redação",
    description="API para avaliação e geração de Redação usando Langgraph e OpenAI",
    version="1.0.0"
)
