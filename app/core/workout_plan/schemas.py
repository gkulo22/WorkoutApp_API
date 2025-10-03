from typing import List, Optional
from pydantic import BaseModel

from app.core import ExerciseForWorkoutPlan
from app.core.workout_plan.models import WorkoutPlan


class CreateWorkoutPlanRequest(BaseModel):
    name: str
    goal_description: str


class CreateWorkoutPlanResponse(BaseModel):
    id: str
    name: str
    exercises: List[ExerciseForWorkoutPlan]
    goal_description: str


class AddStrengthExerciseInWorkoutPlanRequest(BaseModel):
    exercise_id: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None


class AddCardioExerciseInWorkoutPlanRequest(BaseModel):
    exercise_id: str
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None


class AddExerciseInWorkoutPlanResponse(BaseModel):
    id: str
    name: str
    exercises: List[ExerciseForWorkoutPlan]
    goal_description: str


class GetOneWorkoutPlanResponse(BaseModel):
    id: str
    name: str
    exercises: List[ExerciseForWorkoutPlan]
    goal_description: str


class GetAllWorkoutPlansResponse(BaseModel):
    workout_plans: List[WorkoutPlan]


