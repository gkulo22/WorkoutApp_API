from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    username: str
    password: str