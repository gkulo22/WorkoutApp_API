from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class WeightEntryResponse(BaseModel):
    id: str
    value: float
    recorded_at: datetime


class WeightEntryRequest(BaseModel):
    value: float
    recorded_at: Optional[datetime] = None


class GetAllWeightEntriesResponse(BaseModel):
    entries: List[WeightEntryResponse]


class FitnessGoalResponse(BaseModel):
    id: str
    name: str
    type: str
    target_value: float
    current_value: float
    is_completed: bool
    created_at: datetime
    due_date: Optional[datetime] = None
    exercise_id: Optional[str] = None
    description: Optional[str] = ""


class GetFitnessGoalsResponse(BaseModel):
    goals: List[FitnessGoalResponse]


class CreateFitnessGoalRequest(BaseModel):
    name: str
    type: str
    target_value: float
    exercise_id: Optional[str] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = ""


class UpdateFitnessGoalRequest(BaseModel):
    name: Optional[str] = None
    target_value: Optional[float] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = None


class UpdateFitnessGoalStatusRequest(BaseModel):
    status: bool


class GetAchievementsResponse(BaseModel):
    achievements: List[FitnessGoalResponse]


class GetSummeryResponse(BaseModel):
    current_weight: Optional[float] = None
    total_goals: int
    completed_goals: int
    active_goals: int
    nearest_goal_due: Optional[datetime] = None