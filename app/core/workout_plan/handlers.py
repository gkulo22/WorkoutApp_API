from abc import ABC, abstractmethod

from app.core import ExerciseForWorkoutPlan, StrengthExercise, CardioExercise
from app.core.workout_plan.builder import StrengthExerciseBuilder, CardioExerciseBuilder


class ExerciseHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    @abstractmethod
    def can_handle(self, exercise_type: str) -> bool:
        pass

    @abstractmethod
    def build(self, exercise_id: str, **kwargs) -> ExerciseForWorkoutPlan:
        pass

    def handle(self, exercise_type: str, exercise_id: str, **kwargs) -> ExerciseForWorkoutPlan:
        if self.can_handle(exercise_type):
            return self.build(exercise_id, **kwargs)
        elif self._next_handler:
            return self._next_handler.handle(
                exercise_type=exercise_type,
                exercise_id=exercise_id,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported exercise type: {exercise_type}")



class StrengthExerciseHandler(ExerciseHandler):
    def can_handle(self, exercise_type: str) -> bool:
        return exercise_type == "strength"

    def build(self, exercise_id: str, **kwargs) -> StrengthExercise:
        return (
            StrengthExerciseBuilder()
            .with_id(exercise_id)
            .with_sets(kwargs.get("sets"))
            .with_reps(kwargs.get("reps"))
            .with_weight(kwargs.get("weight"))
            .build()
        )


class CardioExerciseHandler(ExerciseHandler):
    def can_handle(self, exercise_type: str) -> bool:
        return exercise_type == "cardio"

    def build(self, exercise_id: str, **kwargs) -> CardioExercise:
        return (
            CardioExerciseBuilder()
            .with_id(exercise_id)
            .with_duration(kwargs.get("duration"))
            .with_distance(kwargs.get("distance"))
            .with_calories(kwargs.get("calories"))
            .build()
        )
