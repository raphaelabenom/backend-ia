from fastapi import FastAPI
from http import HTTPStatus
from schemas import UserSchema, UserPublic

app = FastAPI()

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
  return user