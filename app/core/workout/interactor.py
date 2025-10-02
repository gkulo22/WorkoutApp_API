from dataclasses import dataclass
from typing import List

from app.core import NO_ID
from app.core.exercise.service import ExerciseService
from app.core.workout.models import WorkoutPlan
from app.core.workout.service import WorkoutPlanService


@dataclass
class WorkoutPlanInteractor:
    workout_plan_service: WorkoutPlanService
    exercise_service: ExerciseService


    def execute_create(self, name: str, goal_description: str) -> WorkoutPlan:
        workout_plan = WorkoutPlan(
            id=NO_ID,
            name=name,
            goal_description=goal_description,
            exercises=[]
        )
        return self.workout_plan_service.create_workout_plan(workout_plan=workout_plan)

    def execute_get_one(self, workout_plan_id: str) -> WorkoutPlan:
        return self.workout_plan_service.get_workout_plan(workout_plan_id=workout_plan_id)

    def execute_get_all(self) -> List[WorkoutPlan]:
        return self.workout_plan_service.get_all_workout_plans()

    def execute_delete(self, workout_plan_id: str) -> None:
        workout_plan = self.workout_plan_service.get_workout_plan(workout_plan_id=workout_plan_id)
        self.workout_plan_service.delete_workout_plan(workout_plan_id=workout_plan.id)

    def execute_add_exercise_in_workout_plan(
            self,
            workout_plan_id: str,
            exercise_id: str,
            exercise_type: str,
            **kwargs
    ) -> WorkoutPlan:
        pass

    def execute_delete_exercise_from_workout_plan(
            self,
            workout_plan_id: str,
            exercise_id: str
    ) -> None:
        workout_plan = self.workout_plan_service.get_workout_plan(workout_plan_id=workout_plan_id)
        self.workout_plan_service.delete_exercise_from_workout_plan(
            workout_plan_id=workout_plan.id,
            exercise_id=exercise_id
        )


