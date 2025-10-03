import sqlite3
import uuid
from dataclasses import dataclass
from typing import Optional, List

from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository
from app.core.factories.repo_factory import RepoFactory
from app.core.user.models import User
from app.core.user.repository import IUserRepository
from app.core.workout.models import WorkoutPlan
from app.core.workout.repository import IWorkoutPlanRepository



@dataclass
class UserSqliteRepository(IUserRepository):
    connection: sqlite3.Connection

    def create(self, user: User) -> User:
        pass

    def get_user(self, username: str) -> Optional[User]:
        pass

    def username_exists(self, username: str) -> bool:
        pass


@dataclass
class ExerciseSqliteRepository(IExerciseRepository):
    connection: sqlite3.Connection

    def create(self, exercise: Exercise) -> Exercise:
        pass

    def get_one(self, exercise_id: str) -> Optional[Exercise]:
        pass

    def get_all(self) -> List[Exercise]:
        pass

    def has_code(self, exercise_code: int) -> bool:
        pass



@dataclass
class WorkoutPlanSqliteRepository(IWorkoutPlanRepository):
    connection: sqlite3.Connection

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




@dataclass
class SqliteRepoFactory(RepoFactory):
    connection: sqlite3.Connection

    def __post_init__(self) -> None:
        pass

    def _initialize_db(self) -> None:
        pass

    def users(self) -> IUserRepository:
        return UserSqliteRepository(self.connection)

    def exercises(self) -> IExerciseRepository:
        return ExerciseSqliteRepository(self.connection)

    def workout_plans(self) -> IWorkoutPlanRepository:
        return WorkoutPlanSqliteRepository(self.connection)
