from utils.logger import logger
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.token import Token
from datetime import datetime, timedelta
from jwt import PyJWTError
import os
import jwt

# Configuração de autenticação
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")

# Rota de autenticação
router = APIRouter(tags=["Authentication"])

# Função para criar token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    logger.debug(f"Criando access token para dados: {data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token JWT criado com sucesso. Expira em: {expire}")
    return encoded_jwt

# Função para verificar token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.debug("Tentando validar token de usuário")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        logger.debug(f"Token decodificado com sucesso para usuário: {username}")
        if username is None:
            logger.warning("Token válido mas sem username")
            raise credentials_exception
        return username
    except PyJWTError as e:
        logger.error(f"Erro ao decodificar token JWT: {str(e)}")
        raise credentials_exception

# Rota para autenticação
@router.post("/v1/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Tentativa de login para usuário: {form_data.username}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    logger.info(f"Login bem-sucedido para usuário: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
