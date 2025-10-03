from dataclasses import dataclass, field


@dataclass
class GetWorkoutSessionException(Exception):
    workout_session_id: str
    message: str = field(init=False)

    def __post_init__(self):
        self.message = f"Workout session with id: {self.workout_session_id} does not exist."