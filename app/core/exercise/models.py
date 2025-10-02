from dataclasses import dataclass
from typing import Optional

from app.core.exercise import Muscle


@dataclass
class Exercise:
    id: str
    name: str
    exercise_code: int
    target_muscle: Muscle
    description: str = ""
    instruction: str = ""



@dataclass
class StrengthExercise:
    id: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None


@dataclass
class CardioExercise:
    id: str
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None