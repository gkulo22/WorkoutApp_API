from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.user.models import User
from app.infra.auth import get_current_user

tracking_api = APIRouter()
user_dependency = Annotated[User, Depends(get_current_user)]


@tracking_api.get("/weight")
def get_weight_history():
    pass


@tracking_api.post("/weight")
def record_weight():
    pass


@tracking_api.get("/weight/latest")
def get_weight_latest():
    pass


@tracking_api.delete("/weight/{entry_id}")
def delete_weight(entry_id: str):
    pass


@tracking_api.get("/goals")
def get_fitness_goals():
    pass


@tracking_api.post("/goals")
def create_fitness_goals():
    pass


@tracking_api.put("/goals/{goal_id}")
def update_fitness_goal(goal_id: str):
    pass


@tracking_api.delete("/goals/{goal_id}")
def delete_fitness_goals(goal_id: str):
    pass


@tracking_api.get("/goals/active")
def get_active_goals():
    pass


@tracking_api.patch("/goals/{goal_id}")
def update_fitness_goal_status(goal_id: str):
    pass


@tracking_api.put("/goals/{goal_id}/progress")
def update_goal_progress(goal_id: str):
    pass


@tracking_api.get("/achievements")
def get_fitness_achievements():
    pass


@tracking_api.get("/summery")
def get_fitness_summery():
    pass
