from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    hashed_password: str