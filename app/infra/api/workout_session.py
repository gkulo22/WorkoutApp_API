from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.user.models import User
from app.infra.auth import get_current_user

workout_session_api = APIRouter()
user_dependency = Annotated[User, Depends(get_current_user)]


@workout_session_api.post("/start/{workout_id}")
def start_workout_session(workout_id: str):
    pass


@workout_session_api.post("/{session_id}/complete")
def complete_workout_session(session_id: str):
    pass


@workout_session_api.get("/{session_id}")
def get_workout_session(session_id: str):
    pass


@workout_session_api.put("/{session_id}/exercise/{exercise_id}/progress")
def update_exercise_progression(session_id: str, exercise_id: str):
    pass


@workout_session_api.post("/{session_id}/exercise/next")
def next_exercise(session_id: str):
    pass
