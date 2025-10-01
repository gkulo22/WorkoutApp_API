from dataclasses import dataclass

from app.core.exercise.interactor import ExerciseInteractor
from app.core.exercise.schemas import CreateExerciseRequest, CreateExerciseResponse, GetAllExercisesResponse, \
    GetOneExerciseResponse
from app.core.exercise.service import ExerciseService
from app.core.factories.repo_factory import RepoFactory


@dataclass
class PWPSCore:
    exercise_interactor: ExerciseInteractor

    @classmethod
    def create(cls, database: RepoFactory) -> 'PWPSCore':
        exercise_service = ExerciseService(database.exercises())
        return cls(exercise_interactor=ExerciseInteractor(
            exercise_service=exercise_service)
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