from typing import Protocol

from app.core.exercise.repository import IExerciseRepository


class RepoFactory(Protocol):
    def exercises(self) -> IExerciseRepository:
        pass