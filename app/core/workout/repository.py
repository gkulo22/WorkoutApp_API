from typing import Protocol, Optional, List

from app.core.workout.models import WorkoutPlan


class IWorkoutPlanRepository(Protocol):
    def create(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass

    def get_one(self, workout_plan_id: str) -> Optional[WorkoutPlan]:
        pass

    def get_all(self, author_id: str) -> List[WorkoutPlan]:
        pass

    def delete(self, workout_plan_id: str) -> None:
        pass

    def add_exercise(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass

    def delete_exercise(self, workout_plan: WorkoutPlan) -> None:
        pass