from dataclasses import dataclass
from typing import List

from app.core import NO_ID
from app.core.exercise.models import Exercise
from app.core.exercise.service import ExerciseService


@dataclass
class ExerciseInteractor:
    exercise_service: ExerciseService

    def execute_create(self,
                       name: str,
                       description: str,
                       instruction: str,
                       target_muscle: str) -> Exercise:

        exercise = Exercise(id=NO_ID,
                            name=name,
                            description=description,
                            instruction=instruction,
                            target_muscle=target_muscle)

        return self.exercise_service.create_exercise(exercise=exercise)

    def execute_get_one(self, exercise_id: str) -> Exercise:
        exercise = self.exercise_service.get_one_exercise(
            exercise_id=exercise_id)
        return exercise

    def execute_get_all(self) -> List[Exercise]:
        return self.exercise_service.get_all_exercises()

