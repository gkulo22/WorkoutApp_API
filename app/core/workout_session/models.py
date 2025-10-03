from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict


@dataclass
class WorkoutSession:
    id: str
    user_id: str
    workout_plan_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_exercise_id: Optional[str] = None
    next_exercise_id: Optional[str] = None
    progress_summary: Dict[str, dict] = field(default_factory=dict)