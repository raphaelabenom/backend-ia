from dotenv import load_dotenv
from extensions import app
import os

from routes.generate_exemplary_essay import router as generate_exemplary_essay_router
from routes.generate_evaluate_essay import router as evaluate_essay_router
from routes.auth import router as auth_router

# Carregue as variáveis de ambiente
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Rotas
app.include_router(generate_exemplary_essay_router)  # Rota com a tag 'Generate Essay'
app.include_router(evaluate_essay_router)  # Rota com a tag 'Evaluate Essay'
app.include_router(auth_router)  # Rota com a tag 'Authentication'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# Para executar use o seguinte comando:
# uvicorn main:app --reload