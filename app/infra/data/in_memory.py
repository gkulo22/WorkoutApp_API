import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional, List

from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository
from app.core.factories.repo_factory import RepoFactory


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
class InMemoryRepoFactory(RepoFactory):
    _exercises: ExerciseInMemoryRepository = field(
        init=False,
        default_factory=ExerciseInMemoryRepository
    )

    def exercises(self) -> IExerciseRepository:
        return self._exercises