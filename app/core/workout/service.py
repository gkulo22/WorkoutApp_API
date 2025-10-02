from dataclasses import dataclass
from typing import List

from app.core import ExerciseForWorkoutPlan
from app.core.workout.builder import WorkoutPlanBuilder
from app.core.workout.exceptions import GetWorkoutPlanException, ExerciseNotFoundInWorkoutPlanException
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

    def delete_exercise_from_workout_plan(self, workout_plan: WorkoutPlan, exercise_id: str) -> None:
        for exercise in workout_plan.exercises:
            if exercise.id == exercise_id:
                workout_plan.exercises.remove(exercise)
                self.workout_plan_repository.delete_exercise(workout_plan=workout_plan)
                return

        raise ExerciseNotFoundInWorkoutPlanException(exercise_id=exercise_id)

    def add_exercise_in_workout_plan(
            self,
            workout_plan: WorkoutPlan,
            exercise: ExerciseForWorkoutPlan
    ) -> WorkoutPlan:
        new_workout_plan = (
            WorkoutPlanBuilder().with_id(workout_plan.id)
                                .with_name(workout_plan.name)
                                .with_goal(workout_plan.goal_description)
                                .add_exercise(exercise)
                                .build()
        )
        return self.workout_plan_repository.add_exercise(workout_plan=new_workout_plan)

