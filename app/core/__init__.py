from typing import Union

from app.core.exercise.models import CardioExercise, StrengthExercise

NO_ID = "NO_ID"
ExerciseForWorkoutPlan = Union[CardioExercise, StrengthExercise]
