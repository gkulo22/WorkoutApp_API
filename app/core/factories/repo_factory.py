from typing import Protocol

from app.core.exercise.repository import IExerciseRepository
from app.core.workout.repository import IWorkoutPlanRepository


class RepoFactory(Protocol):
    def exercises(self) -> IExerciseRepository:
        pass

    def workout_plans(self) -> IWorkoutPlanRepository:
        pass