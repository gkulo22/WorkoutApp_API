from dataclasses import dataclass
from typing import Optional

from app.core import NO_ID
from app.core.user.models import User
from app.core.user.service import UserService


@dataclass
class UserInteractor:
    user_service: UserService

    def execute_create(self, username: str, hashed_password: str) -> User:
        user = User(id=NO_ID, username=username, hashed_password=hashed_password)
        return self.user_service.create_user(user=user)

    def execute_get_user(self, username: str) -> Optional[User]:
        return self.user_service.get_user(username=username)
