from dataclasses import dataclass, field


@dataclass
class UsernameInUseException(Exception):
    username: str
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"User with username: {self.username} already exists."