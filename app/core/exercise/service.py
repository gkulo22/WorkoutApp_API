from dataclasses import dataclass
from typing import List

from app.core.exercise.exceptions import ExerciseCreationException, GetExerciseException
from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository


@dataclass
class ExerciseService:
    exercise_repository: IExerciseRepository

    def create_exercise(self, exercise: Exercise) -> Exercise:
        if self.exercise_repository.has_code(exercise_code=exercise.exercise_code):
            raise ExerciseCreationException(exercise_code=exercise.exercise_code)
        exercise = self.exercise_repository.create(exercise=exercise)
        return exercise

    def get_one_exercise(self, exercise_id: str) -> Exercise:
        exercise = self.exercise_repository.get_one(exercise_id)
        if not exercise:
            raise GetExerciseException(exercise_id=exercise_id)

        return exercise

    def get_all_exercises(self) -> List[Exercise]:
        return self.exercise_repository.get_all()