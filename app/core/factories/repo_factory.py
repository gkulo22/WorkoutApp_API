from typing import Protocol

from app.core.exercise.repository import IExerciseRepository
from app.core.user.repository import IUserRepository
from app.core.workout.repository import IWorkoutPlanRepository


class RepoFactory(Protocol):
    def users(self) -> IUserRepository:
        pass

    def exercises(self) -> IExerciseRepository:
        pass

    def workout_plans(self) -> IWorkoutPlanRepository:
        pass