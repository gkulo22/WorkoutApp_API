from typing import List

from pydantic import BaseModel

from app.core.exercise import Muscle
from app.core.exercise.models import Exercise


class CreateExerciseRequest(BaseModel):
    name: str
    exercise_code: int
    description: str
    instruction: str
    target_muscle: Muscle


class CreateExerciseResponse(BaseModel):
    exercise: Exercise


class GetAllExercisesResponse(BaseModel):
    exercises: List[Exercise]


class GetOneExerciseResponse(BaseModel):
    name: str
    exercise_code: int
    description: str
    instruction: str
    target_muscle: Muscle
