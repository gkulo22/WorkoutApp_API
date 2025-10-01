from typing import List

from pydantic import BaseModel

from app.core.exercise.models import Exercise


class CreateExerciseRequest(BaseModel):
    name: str
    description: str
    instruction: str
    target_muscle: str


class CreateExerciseResponse(BaseModel):
    exercise: Exercise


class GetAllExercisesResponse(BaseModel):
    exercises: List[Exercise]


class GetOneExerciseResponse(BaseModel):
    name: str
    description: str
    instruction: str
    target_muscle: str
