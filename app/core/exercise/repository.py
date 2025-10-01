from typing import Protocol, List, Optional

from app.core.exercise.models import Exercise


class IExerciseRepository(Protocol):
    def create(self, exercise: Exercise) -> Exercise:
        pass

    def get_one(self, exercise_id: str) -> Optional[Exercise]:
        pass

    def get_all(self) -> List[Exercise]:
        pass