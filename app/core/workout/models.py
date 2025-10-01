from dataclasses import dataclass
from typing import List

from app.core import ExerciseForWorkoutPlan


@dataclass
class WorkoutPlan:
    id: str
    name: str
    exercises: List[ExerciseForWorkoutPlan]
    goal_description: str