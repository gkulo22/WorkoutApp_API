from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.facade import PWPSCore
from app.core.user.schemas import CreateUserRequest
from app.infra.auth import bcrypt_context, authenticate_user, create_access_token
from app.infra.dependables import get_core

auth_api = APIRouter()

class CreateUserBase(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


@auth_api.post("", status_code=HTTPStatus.CREATED)
async def create_user(request: CreateUserBase, core: PWPSCore = Depends(get_core)) -> None:
    core.create_user(
        request=CreateUserRequest(
            username=request.username,
            password=bcrypt_context.hash(request.password)
        )
    )


@auth_api.post("/token", response_model=Token)
async def login_for_access_token(
        from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        core: PWPSCore = Depends(get_core)
) -> Token:
    user = authenticate_user(from_data.username, from_data.password, core)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return Token(access_token=token, token_type="bearer")
