from dataclasses import field, dataclass


@dataclass
class GetExerciseException(Exception):
    exercise_id: str
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"Exercise with id: {self.exercise_id} does not exist."


@dataclass
class ExerciseCreationException(Exception):
    exercise_code: int
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"Exercise with code: {self.exercise_code} already exists."