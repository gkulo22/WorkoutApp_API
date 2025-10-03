from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.facade import PWPSCore
from app.core.user.models import User
from app.core.workout_session.schemas import (
    CreateWorkoutSessionResponse,
    WorkoutSessionProgressRequest,
    WorkoutSessionProgressResponse,
    WorkoutSessionResponse,
)
from app.infra.auth import get_current_user
from app.infra.dependables import get_core

workout_session_api = APIRouter()
user_dependency = Annotated[User, Depends(get_current_user)]


@workout_session_api.post("/start/{workout_id}",
                          status_code=HTTPStatus.CREATED,
                          response_model=CreateWorkoutSessionResponse
                          )
def start_workout_session(
        workout_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> CreateWorkoutSessionResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")

    return core.start_workout_session(workout_id=workout_id, user_id=user.id)


@workout_session_api.post("/{session_id}/complete",
                          status_code=HTTPStatus.OK,
                          response_model=WorkoutSessionResponse
                          )
def complete_workout_session(
        session_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WorkoutSessionResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.complete_workout_session(session_id=session_id, user_id=user.id)


@workout_session_api.get("/{session_id}",
                         status_code=HTTPStatus.OK,
                         response_model=WorkoutSessionResponse
                         )
def get_workout_session(
        session_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WorkoutSessionResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_workout_session(session_id=session_id, user_id=user.id)




class ProgressBase(BaseModel):
    sets_completed: Optional[int] = None
    reps_last_set: Optional[int] = None
    weight_last_set: Optional[float] = None
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None
    mark_complete: bool = False
    notes: Optional[str] = None



@workout_session_api.put("/{session_id}/exercise/{exercise_id}/progress",
                         status_code=HTTPStatus.OK,
                         response_model=WorkoutSessionProgressResponse)
def update_exercise_progression(
        session_id: str,
        exercise_id: str,
        request: ProgressBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WorkoutSessionProgressResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.update_exercise_progression(
        session_id=session_id,
        user_id=user.id,
        exercise_id=exercise_id,
        request=WorkoutSessionProgressRequest(**request.dict())
    )


@workout_session_api.post("/{session_id}/exercise/next",
                          status_code=HTTPStatus.OK,
                          response_model=WorkoutSessionResponse
                          )
def next_exercise(
        session_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WorkoutSessionResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.move_to_next_exercise(session_id=session_id, user_id=user.id)
