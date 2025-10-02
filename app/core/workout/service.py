from dataclasses import dataclass
from typing import List

from app.core.workout.exceptions import GetWorkoutPlanException
from app.core.workout.models import WorkoutPlan
from app.core.workout.repository import IWorkoutPlanRepository


@dataclass
class WorkoutPlanService:
    workout_plan_repository: IWorkoutPlanRepository

    def create_workout_plan(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        return self.workout_plan_repository.create(workout_plan=workout_plan)

    def get_workout_plan(self, workout_plan_id: str) -> WorkoutPlan:
        workout_plan = self.workout_plan_repository.get_one(workout_plan_id=workout_plan_id)
        if not WorkoutPlan:
            raise GetWorkoutPlanException(workout_plan_id=workout_plan_id)

        return workout_plan

    def get_all_workout_plans(self) -> List[WorkoutPlan]:
        return self.workout_plan_repository.get_all()

    def delete_workout_plan(self, workout_plan_id: str) -> None:
        self.workout_plan_repository.delete(workout_plan_id=workout_plan_id)

    def delete_exercise_from_workout_plan(self, workout_plan_id: str, exercise_id: str):
        self.workout_plan_repository.delete_exercise(
            workout_plan_id=workout_plan_id,
            exercise_id=exercise_id
        )

