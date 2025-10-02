from dataclasses import dataclass

from app.core.exercise.interactor import ExerciseInteractor
from app.core.exercise.schemas import CreateExerciseRequest, CreateExerciseResponse, GetAllExercisesResponse, \
    GetOneExerciseResponse
from app.core.exercise.service import ExerciseService
from app.core.factories.repo_factory import RepoFactory
from app.core.workout.interactor import WorkoutPlanInteractor
from app.core.workout.schemas import CreateWorkoutPlanRequest, CreateWorkoutPlanResponse, GetOneWorkoutPlanResponse, \
    AddExerciseInWorkoutPlanResponse, AddCardioExerciseInWorkoutPlanRequest, \
    AddStrengthExerciseInWorkoutPlanRequest
from app.core.workout.service import WorkoutPlanService


@dataclass
class PWPSCore:
    exercise_interactor: ExerciseInteractor
    workout_plan_interactor: WorkoutPlanInteractor

    @classmethod
    def create(cls, database: RepoFactory) -> 'PWPSCore':
        exercise_service = ExerciseService(database.exercises())
        workout_plan_service = WorkoutPlanService(database.workout_plans())
        return cls(
            exercise_interactor=ExerciseInteractor(
                exercise_service=exercise_service
            ),
            workout_plan_interactor=WorkoutPlanInteractor(
                exercise_service=exercise_service,
                workout_plan_service=workout_plan_service
            )
        )

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
    def create_workout_plan(self, request: CreateWorkoutPlanRequest) -> CreateWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_create(
            name=request.name,
            goal_description=request.goal_description
        )

        return CreateWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def get_one_workout_plan(self, workout_plan_id: str) -> GetOneWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_get_one(workout_plan_id=workout_plan_id)
        return GetOneWorkoutPlanResponse(
            id=workout_plan.id,
            name=workout_plan.name,
            exercises=workout_plan.exercises,
            goal_description=workout_plan.goal_description
        )

    def add_strength_exercise_in_workout_plan(
            self,
            workout_plan_id: str,
            request: AddStrengthExerciseInWorkoutPlanRequest) -> AddExerciseInWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_add_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
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
            request: AddCardioExerciseInWorkoutPlanRequest) -> AddExerciseInWorkoutPlanResponse:
        workout_plan = self.workout_plan_interactor.execute_add_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
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

    def delete_workout_plan(self, workout_plan_id: str) -> None:
        self.workout_plan_interactor.execute_delete(workout_plan_id=workout_plan_id)

    def delete_exercise_from_workout_plan(self, workout_plan_id: str, exercise_id: str) -> None:
        self.workout_plan_interactor.execute_delete_exercise_from_workout_plan(
            workout_plan_id=workout_plan_id,
            exercise_id=exercise_id
        )