from dataclasses import dataclass
from typing import Optional

from app.core.exercise.interactor import ExerciseInteractor
from app.core.exercise.schemas import CreateExerciseRequest, CreateExerciseResponse, GetAllExercisesResponse, \
    GetOneExerciseResponse
from app.core.exercise.service import ExerciseService
from app.core.factories.repo_factory import RepoFactory
from app.core.tracking.schemas import GetAllWeightEntriesResponse, WeightEntryRequest, WeightEntryResponse, \
    GetFitnessGoalsResponse, FitnessGoalResponse, CreateFitnessGoalRequest, UpdateFitnessGoalRequest, \
    UpdateFitnessGoalStatusRequest, GetAchievementsResponse, GetSummeryResponse
from app.core.user.interactor import UserInteractor
from app.core.user.models import User
from app.core.user.schemas import CreateUserRequest
from app.core.user.service import UserService
from app.core.workout_plan.interactor import WorkoutPlanInteractor
from app.core.workout_plan.schemas import CreateWorkoutPlanRequest, CreateWorkoutPlanResponse, \
    GetOneWorkoutPlanResponse, \
    AddExerciseInWorkoutPlanResponse, AddCardioExerciseInWorkoutPlanRequest, \
    AddStrengthExerciseInWorkoutPlanRequest, GetAllWorkoutPlansResponse, UpdateWorkoutPlanStatusRequest
from app.core.workout_plan.service import WorkoutPlanService
from app.core.workout_session.schemas import CreateWorkoutSessionResponse, WorkoutSessionResponse, \
    WorkoutSessionProgressRequest, WorkoutSessionProgressResponse


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

    def change_privacy_status(
            self,
            workout_plan_id: str,
            request: UpdateWorkoutPlanStatusRequest
    ) -> None:
        pass

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


    # Workout Sessions
    def start_workout_session(self, workout_id: str, user_id: str) -> CreateWorkoutSessionResponse:
        pass

    def complete_workout_session(self, session_id: str, user_id: str) -> WorkoutSessionResponse:
        pass

    def get_workout_session(self, session_id: str, user_id: str) -> WorkoutSessionResponse:
        pass

    def update_exercise_progression(
            self,
            session_id: str,
            user_id: str,
            exercise_id: str,
            request: WorkoutSessionProgressRequest
    ) -> WorkoutSessionProgressResponse:
        pass

    def move_to_next_exercise(self, session_id: str, user_id: str) -> WorkoutSessionResponse:
        pass


    # Tracking and Goals
    def get_weight_history(self, user_id: str) -> GetAllWeightEntriesResponse:
        pass

    def record_weight(
            self,
            user_id: str,
            request: WeightEntryRequest
    ) -> WeightEntryResponse:
        pass

    def get_latest_weight(self, user_id: str) -> WeightEntryResponse:
        pass

    def delete_weight(self, user_id: str, entry_id: str) -> None:
        pass

    def get_fitness_goals(self, user_id: str) -> GetFitnessGoalsResponse:
        pass

    def create_fitness_goals(
            self,
            user_id: str,
            request: CreateFitnessGoalRequest
    ) -> FitnessGoalResponse:
        pass

    def update_fitness_goal(
            self,
            goal_id: str,
            user_id: str,
            request: UpdateFitnessGoalRequest
    ) -> FitnessGoalResponse:
        pass

    def delete_fitness_goals(self, user_id: str, goal_id: str) -> None:
        pass

    def get_active_goals(self, user_id: str) -> GetFitnessGoalsResponse:
        pass

    def update_fitness_goal_status(
            self,
            goal_id: str,
            request: UpdateFitnessGoalStatusRequest
    ) -> None:
        pass

    def update_goal_progress(
            self,
            goal_id: str,
            user_id: str,
            current_value: float
    ) -> FitnessGoalResponse:
        pass

    def get_fitness_achievements(self, user_id: str) -> GetAchievementsResponse:
        pass

    def get_user_fitness_summery(self, user_id: str) -> GetSummeryResponse:
        pass



