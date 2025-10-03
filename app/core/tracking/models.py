from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeightEntry:
    id: str
    user_id: str
    value: float
    recorded_at: datetime


@dataclass
class FitnessGoal:
    id: str
    user_id: str
    name: str
    type: str
    target_value: float
    current_value: float
    is_completed: bool
    created_at: datetime
    due_date: Optional[datetime] = None
    exercise_id: Optional[str] = None
    description: str = ""


