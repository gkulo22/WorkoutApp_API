from dataclasses import dataclass, field


@dataclass
class ExerciseNotFoundInWorkoutPlanException(Exception):
    exercise_id: str
    message: str = field(init=False)

    def __post_init__(self):
        self.message = f"Exercise with id: {self.exercise_id} does not exist in workout plan."


@dataclass
class GetWorkoutPlanException(Exception):
    workout_plan_id: str
    message: str = field(init=False)

    def __post_init__(self):
        self.message = f"Workout plan with id: {self.workout_plan_id} does not exist."


