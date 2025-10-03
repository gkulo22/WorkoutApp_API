from abc import ABC, abstractmethod

from app.core.workout_plan.models import WorkoutPlan


class WorkoutPlanState(ABC):
    @abstractmethod
    def change_status(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass


class PrivateWorkoutPlanState(WorkoutPlanState):
    def change_status(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass


class PublicWorkoutPlanState(WorkoutPlanState):
    def change_status(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        pass