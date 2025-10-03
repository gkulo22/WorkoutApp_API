from dataclasses import dataclass
from typing import Optional

from app.core.exercise.interactor import ExerciseInteractor
from app.core.exercise.schemas import CreateExerciseRequest, CreateExerciseResponse, GetAllExercisesResponse, \
    GetOneExerciseResponse
from app.core.exercise.service import ExerciseService
from app.core.factories.repo_factory import RepoFactory
from app.core.user.interactor import UserInteractor
from app.core.user.models import User
from app.core.user.schemas import CreateUserRequest
from app.core.user.service import UserService
from app.core.workout.interactor import WorkoutPlanInteractor
from app.core.workout.schemas import CreateWorkoutPlanRequest, CreateWorkoutPlanResponse, GetOneWorkoutPlanResponse, \
    AddExerciseInWorkoutPlanResponse, AddCardioExerciseInWorkoutPlanRequest, \
    AddStrengthExerciseInWorkoutPlanRequest, GetAllWorkoutPlansResponse
from app.core.workout.service import WorkoutPlanService


@dataclass
class PWPSCore:
    user_interactor: UserInteractor
    exercise_interactor: ExerciseInteractor
    workout_plan_interactor: WorkoutPlanInteractor

    @classmethod
    def create(cls, database: RepoFactory) -> 'PWPSCore':
        user_service = UserService(database.users())
        exercise_service = ExerciseService(database.exercises())
        workout_plan_service = WorkoutPlanService(database.workout_plans())
        return cls(
            user_interactor=UserInteractor(
                user_service=user_service
            ),
            exercise_interactor=ExerciseInteractor(
                exercise_service=exercise_service
            ),
            workout_plan_interactor=WorkoutPlanInteractor(
                exercise_service=exercise_service,
                workout_plan_service=workout_plan_service
            )
        )

    # Users
    def create_user(self, request: CreateUserRequest) -> None:
        self.user_interactor.execute_create(
            username=request.username,
            hashed_password=request.password
        )

    def get_user(self, username: str) -> Optional[User]:
        return self.user_interactor.execute_get_user(username=username)


    # Exercises
    def create_exercise(self, request: CreateExerciseRequest) -> CreateExerciseResponse:
        exercise = self.exercise_interactor.execute_create(
            name=request.name,
            exercise_code=request.exercise_code,
            description=request.description,
            instruction=request.instruction,
            target_muscle=request.target_muscle
        )
        return CreateExerciseResponse(exercise=exercise)

    def get_all_exercises(self) -> GetAllExercisesResponse:
        exercises = self.exercise_interactor.execute_get_all()
        return GetAllExercisesResponse(exercises=exercises)

    def get_one_exercise(self, exercise_id: str) -> GetOneExerciseResponse:
        exercise = self.exercise_interactor.execute_get_one(exercise_id=exercise_id)
        return GetOneExerciseResponse(
            name=exercise.name,
            exercise_code=exercise.exercise_code,
            description=exercise.description,
            instruction=exercise.instruction,
            target_muscle=exercise.target_muscle
        )



    # Workout Plans
    def create_workout_plan(
            self,
            user_id:str,
            request: CreateWorkoutPlanRequest
    ) -> CreateWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_create(
            author_id=user_id,
            name=request.name,
            goal_description=request.goal_description
        )

        return CreateWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def get_one_workout_plan(
            self,
            user_id: str,
            workout_plan_id: str
    ) -> GetOneWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_get_one(
            author_id=user_id,
            workout_plan_id=workout_plan_id
        )
        return GetOneWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def get_all_workout_plans(self, user_id: str) -> GetAllWorkoutPlansResponse:
        workout_plans = self.workout_plan_interactor.execute_get_all(author_id=user_id)
        return GetAllWorkoutPlansResponse(workout_plans=workout_plans)

    def add_strength_exercise_in_workout_plan(
            self,
            workout_plan_id: str,
            user_id: str,
            request: AddStrengthExerciseInWorkoutPlanRequest) -> AddExerciseInWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_add_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=user_id,
            exercise_id=request.exercise_id,
            exercise_type="strength",
            sets=request.sets,
            reps=request.reps,
            weight=request.weight,
        )

        return AddExerciseInWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def add_cardio_exercise_in_workout_plan(
            self,
            workout_plan_id: str,
            user_id: str,
            request: AddCardioExerciseInWorkoutPlanRequest) -> AddExerciseInWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_add_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=user_id,
            exercise_id=request.exercise_id,
            exercise_type="cardio",
            duration=request.duration,
            distance=request.distance,
            calories=request.calories,
        )

        return AddExerciseInWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def delete_workout_plan(self, workout_plan_id: str, user_id: str) -> None:
        self.workout_plan_interactor.execute_delete(
            workout_plan_id=workout_plan_id,
            author_id=user_id
        )

    def delete_exercise_from_workout_plan(
            self,
            workout_plan_id: str,
            user_id: str,
            exercise_id: str
    ) -> None:
        self.workout_plan_interactor.execute_delete_exercise_from_workout_plan(
            workout_plan_id=workout_plan_id,
            author_id=user_id,
            exercise_id=exercise_id
        )