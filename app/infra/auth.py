from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from app.core.facade import PWPSCore
from app.core.user.models import User
from app.infra.dependables import get_core

SECRET_KEY = '197b2c37c391bed93fe80344fe73806947a65e36206e05a1a23c2fa12702e3'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

def authenticate_user(username: str, password: str, core: PWPSCore) -> Optional[User]:
    user = core.get_user(username=username)
    if not user:
        return None

    if not bcrypt_context.verify(password, user.hashed_password):
        return None

    return user


def create_access_token(username: str, user_id: str, expires_delta: timedelta) -> str:
    encode = {'sub': username, 'id': user_id}
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_bearer)],
        core: PWPSCore = Depends(get_core)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )

        user = core.get_user(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )
