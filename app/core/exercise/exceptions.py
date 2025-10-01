from dataclasses import field, dataclass


@dataclass
class GetExerciseException(Exception):
    exercise_id: str
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"Exercise with id: {self.exercise_id} does not exist."


@dataclass
class ExerciseCreationException(Exception):
    barcode: str
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"Exercise with barcode: {self.barcode} already exists."