from typing import List, Optional

from app.core import StrengthExercise, CardioExercise, ExerciseForWorkoutPlan, NO_ID
from app.core.workout.models import WorkoutPlan


class StrengthExerciseBuilder:
    def __init__(self):
        self._id = NO_ID
        self._sets = None
        self._reps = None
        self._weight = None

    def with_id(self, exercise_id: str):
        self._id = exercise_id
        return self

    def with_sets(self, sets: int):
        if sets is not None and sets <= 0:
            raise ValueError("sets must be greater than 0")
        self._sets = sets
        return self

    def with_reps(self, reps: int):
        if reps is not None and reps <= 0:
            raise ValueError("reps must be greater than 0")
        self._reps = reps
        return self

    def with_weight(self, weight: float):
        if weight is not None and weight <= 0:
            raise ValueError("weight must be greater than 0")
        self._weight = weight
        return self

    def build(self) -> StrengthExercise:
        if (self._sets is None) ^ (self._reps is None):
            raise ValueError("Both 'sets' and 'reps' must be provided together or omitted together")

        return StrengthExercise(
            id=self._id,
            sets=self._sets,
            reps=self._reps,
            weight=self._weight,
        )



class CardioExerciseBuilder:
    def __init__(self):
        self._id = NO_ID
        self._duration: Optional[float] = None
        self._distance: Optional[float] = None
        self._calories: Optional[float] = None

    def with_id(self, exercise_id: str):
        self._id = exercise_id
        return self

    def with_duration(self, duration: float):
        if duration is not None and duration <= 0:
            raise ValueError("duration must be greater than 0")
        self._duration = duration
        return self

    def with_distance(self, distance: float):
        if distance is not None and distance <= 0:
            raise ValueError("distance must be greater than 0")
        self._distance = distance
        return self

    def with_calories(self, calories: float):
        if calories is not None and calories <= 0:
            raise ValueError("calories must be greater than 0")
        self._calories = calories
        return self

    def build(self) -> CardioExercise:
        if all(v is None for v in (self._duration, self._distance, self._calories)):
            raise ValueError(
                "At least one of 'duration', 'distance', or 'calories' must be provided"
            )

        return CardioExercise(
            id=self._id,
            duration=self._duration,
            distance=self._distance,
            calories=self._calories,
        )



class WorkoutPlanBuilder:
    def __init__(self):
        self._id = NO_ID
        self._name = "Unnamed"
        self._goal_description = ""
        self._exercises: List[ExerciseForWorkoutPlan] = []

    def with_id(self, workout_plan_id: str):
        self._id = workout_plan_id
        return self

    def with_name(self, name: str):
        self._name = name
        return self

    def with_goal(self, description: str):
        self._goal_description = description
        return self

    def add_exercise(self, exercise: ExerciseForWorkoutPlan):
        self._exercises.append(exercise)
        return self

    def build(self) -> WorkoutPlan:
        return WorkoutPlan(
            id=self._id,
            name=self._name,
            exercises=self._exercises,
            goal_description=self._goal_description,
        )
