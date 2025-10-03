from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class CreateWorkoutSessionResponse(BaseModel):
    session_id: str
    workout_plan_id: str
    user_id: str
    started_at: datetime


class WorkoutSessionResponse(BaseModel):
    id: str
    workout_plan_id: str
    user_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_exercise_id: Optional[str] = None
    next_exercise_id: Optional[str] = None
    progress_summary: Dict[str, Any] = {}


class WorkoutSessionProgressRequest(BaseModel):
    sets_completed: Optional[int] = None
    reps_last_set: Optional[int] = None
    weight_last_set: Optional[float] = None
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None
    mark_complete: bool = False
    notes: Optional[str] = None


class WorkoutSessionProgressResponse(BaseModel):
    session: WorkoutSessionResponse