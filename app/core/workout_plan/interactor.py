from dataclasses import dataclass
from typing import List

from app.core.exercise.service import ExerciseService
from app.core.workout_plan.builder import WorkoutPlanBuilder
from app.core.workout_plan.handlers import StrengthExerciseHandler, CardioExerciseHandler
from app.core.workout_plan.models import WorkoutPlan
from app.core.workout_plan.service import WorkoutPlanService


@dataclass
class WorkoutPlanInteractor:
    workout_plan_service: WorkoutPlanService
    exercise_service: ExerciseService


    def execute_create(
            self,
            author_id: str,
            name: str,
            goal_description: str
    ) -> WorkoutPlan:
        workout_plan = (
            WorkoutPlanBuilder().with_name(name=name)
                                .with_goal(description=goal_description)
                                .with_author(author_id=author_id)
                                .build()
        )
        return self.workout_plan_service.create_workout_plan(workout_plan=workout_plan)

    def execute_get_one(self, author_id: str, workout_plan_id: str) -> WorkoutPlan:
        return self.workout_plan_service.get_workout_plan(
            author_id=author_id,
            workout_plan_id=workout_plan_id
        )

    def execute_get_all(self, author_id: str) -> List[WorkoutPlan]:
        return self.workout_plan_service.get_all_workout_plans(author_id=author_id)

    def execute_delete(self, workout_plan_id: str, author_id: str) -> None:
        workout_plan = self.workout_plan_service.get_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=author_id
        )
        self.workout_plan_service.delete_workout_plan(workout_plan_id=workout_plan.id)

    def execute_add_exercise_in_workout_plan(
            self,
            workout_plan_id: str,
            author_id: str,
            exercise_id: str,
            exercise_type: str,
            **kwargs
    ) -> WorkoutPlan:
        exercise = self.exercise_service.get_one_exercise(exercise_id=exercise_id)

        strength_handler = StrengthExerciseHandler(next_handler=CardioExerciseHandler())
        exercise_to_add = strength_handler.handle(
            exercise_type=exercise_type,
            exercise_id=exercise.id,
            **kwargs
        )

        workout_plan = self.workout_plan_service.get_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=author_id,
        )
        return self.workout_plan_service.add_exercise_in_workout_plan(
            workout_plan=workout_plan,
            exercise=exercise_to_add
        )


    def execute_delete_exercise_from_workout_plan(
            self,
            workout_plan_id: str,
            author_id: str,
            exercise_id: str
    ) -> None:
        workout_plan = self.workout_plan_service.get_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=author_id,
        )
        exercise = self.exercise_service.get_one_exercise(exercise_id=exercise_id)
        self.workout_plan_service.delete_exercise_from_workout_plan(
            workout_plan=workout_plan,
            exercise_id=exercise.id
        )


