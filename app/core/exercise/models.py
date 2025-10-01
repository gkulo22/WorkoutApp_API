from dataclasses import dataclass


@dataclass
class Exercise:
    id: str
    name: str
    description: str
    instruction: str
    target_muscle: str