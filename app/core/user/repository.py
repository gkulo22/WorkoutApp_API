from typing import Protocol, Optional

from app.core.user.models import User


class IUserRepository(Protocol):
    def create(self, user: User) -> User:
        pass

    def get_user(self, username: str) -> Optional[User]:
        pass

    def username_exists(self, username: str) -> bool:
        pass