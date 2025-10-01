from dataclasses import dataclass
from typing import Optional

from app.core.exercise import Muscle


@dataclass
class Exercise:
    id: str
    name: str
    exercise_code: int
    description: str
    instruction: str
    target_muscle: Muscle



@dataclass
class StrengthExercise:
    id: str
    sets: int
    reps: int
    weight: float


@dataclass
class CardioExercise:
    id: str
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None