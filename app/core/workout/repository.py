from typing import Protocol

from app.core.workout.models import WorkoutPlan


class IWorkoutPlanRepository(Protocol):
    def create(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass

