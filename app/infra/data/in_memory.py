import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional, List

from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository
from app.core.factories.repo_factory import RepoFactory
from app.core.user.models import User
from app.core.user.repository import IUserRepository
from app.core.workout_plan.models import WorkoutPlan
from app.core.workout_plan.repository import IWorkoutPlanRepository



@dataclass
class UserInMemoryRepository:
    _store: Dict[str, User] = field(default_factory=dict)

    def create(self, user: User) -> User:
        user_id = str(uuid.uuid4())
        setattr(user, 'id', user_id)
        self._store[user.id] = user
        return user

    def get_user(self, username: str) -> Optional[User]:
        for user in self._store.values():
            if user.username == username:
                return user

    def username_exists(self, username: str) -> bool:
        return any(user.username == username for user in self._store.values())


@dataclass
class ExerciseInMemoryRepository(IExerciseRepository):
    _store: Dict[str, Exercise] = field(default_factory=dict)

    def create(self, exercise: Exercise) -> Exercise:
        exercise_id = str(uuid.uuid4())
        setattr(exercise, "id", exercise_id)
        self._store[exercise_id] = exercise
        return exercise

    def get_one(self, exercise_id: str) -> Optional[Exercise]:
        return self._store.get(exercise_id)

    def get_all(self) -> List[Exercise]:
        return list(self._store.values())

    def has_code(self, exercise_code: int) -> bool:
        return any(exercise.exercise_code == exercise_code for exercise in self._store.values())



@dataclass
class WorkoutPlanInMemoryRepository(IWorkoutPlanRepository):
    _store: Dict[str, WorkoutPlan] = field(default_factory=dict)

    def create(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        workout_plan_id = str(uuid.uuid4())
        setattr(workout_plan, "id", workout_plan_id)
        self._store[workout_plan_id] = workout_plan
        return workout_plan

    def get_one(self, workout_plan_id: str) -> Optional[WorkoutPlan]:
        return self._store.get(workout_plan_id)

    def get_all(self, author_id: str) -> List[WorkoutPlan]:
        needed_plans = []
        for workout_plan in self._store.values():
            if workout_plan.author_id == author_id:
                needed_plans.append(workout_plan)
        return needed_plans

    def delete(self, workout_plan_id: str) -> None:
        self._store.pop(workout_plan_id)

    def add_exercise(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        self._store[workout_plan.id] = workout_plan
        return workout_plan

    def delete_exercise(self, workout_plan: WorkoutPlan) -> None:
        self._store[workout_plan.id] = workout_plan





@dataclass
class InMemoryRepoFactory(RepoFactory):
    _users: UserInMemoryRepository = field(
        init=False,
        default_factory=UserInMemoryRepository
    )

    _exercises: ExerciseInMemoryRepository = field(
        init=False,
        default_factory=ExerciseInMemoryRepository
    )

    _workout_plans: WorkoutPlanInMemoryRepository = field(
        init=False,
        default_factory=WorkoutPlanInMemoryRepository
    )

    def users(self) -> IUserRepository:
        return self._users

    def exercises(self) -> IExerciseRepository:
        return self._exercises

    def workout_plans(self) -> IWorkoutPlanRepository:
        return self._workout_plans