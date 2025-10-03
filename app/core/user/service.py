from dataclasses import dataclass
from typing import Optional

from app.core.user.exceptions import UsernameInUseException
from app.core.user.models import User
from app.core.user.repository import IUserRepository


@dataclass
class UserService:
    user_repository: IUserRepository

    def create_user(self, user: User) -> User:
        if self.user_repository.username_exists(username=user.username):
            raise UsernameInUseException(username=user.username)
        return self.user_repository.create(user)

    def get_user(self, username: str) -> Optional[User]:
        return self.user_repository.get_user(username)
