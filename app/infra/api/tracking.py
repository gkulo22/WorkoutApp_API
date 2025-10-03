from datetime import datetime
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.facade import PWPSCore
from app.core.tracking.schemas import (
    CreateFitnessGoalRequest,
    FitnessGoalResponse,
    GetAchievementsResponse,
    GetAllWeightEntriesResponse,
    GetFitnessGoalsResponse,
    GetSummeryResponse,
    UpdateFitnessGoalRequest,
    UpdateFitnessGoalStatusRequest,
    WeightEntryRequest,
    WeightEntryResponse,
)
from app.core.user.models import User
from app.infra.auth import get_current_user
from app.infra.dependables import get_core

tracking_api = APIRouter()
user_dependency = Annotated[User, Depends(get_current_user)]


@tracking_api.get("/weight",
                  status_code=HTTPStatus.OK,
                  response_model=GetAllWeightEntriesResponse)
def get_weight_history(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetAllWeightEntriesResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_weight_history(user_id=user.id)



class RecordWeightBase(BaseModel):
    value: float
    recorded_at: Optional[datetime] = None


@tracking_api.post("/weight",
                   status_code=HTTPStatus.CREATED,
                   response_model=WeightEntryResponse)
def record_weight(
        request: RecordWeightBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WeightEntryResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.record_weight(user_id=user.id, request=WeightEntryRequest(**request.dict()))


@tracking_api.get("/weight/latest",
                  status_code=HTTPStatus.OK,
                  response_model=WeightEntryResponse)
def get_weight_latest(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> WeightEntryResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_latest_weight(user_id=user.id)


@tracking_api.delete("/weight/{entry_id}", status_code=HTTPStatus.OK)
def delete_weight(
        entry_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.delete_weight(user_id=user.id, entry_id=entry_id)


@tracking_api.get("/goals",
                  status_code=HTTPStatus.OK,
                  response_model=GetFitnessGoalsResponse)
def get_fitness_goals(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetFitnessGoalsResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_fitness_goals(user_id=user.id)



class FitnessGoalBase(BaseModel):
    name: str
    type: str
    target_value: float
    exercise_id: Optional[str] = None
    due_date: Optional[datetime] = None
    description: Optional[str] = ""


@tracking_api.post("/goals",
                   status_code=HTTPStatus.CREATED,
                   response_model=FitnessGoalResponse)
def create_fitness_goals(
        request: FitnessGoalBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> FitnessGoalResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.create_fitness_goals(user_id=user.id, request=CreateFitnessGoalRequest(**request.dict()))


@tracking_api.put("/goals/{goal_id}",
                  status_code=HTTPStatus.OK,
                  response_model=FitnessGoalResponse)
def update_fitness_goal(
        goal_id: str,
        request: FitnessGoalBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> FitnessGoalResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.update_fitness_goal(
        goal_id=goal_id,
        user_id=user.id,
        request=UpdateFitnessGoalRequest(**request.dict())
    )


@tracking_api.delete("/goals/{goal_id}", status_code=HTTPStatus.OK)
def delete_fitness_goals(
        goal_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.delete_fitness_goals(user_id=user.id, goal_id=goal_id)


@tracking_api.get("/goals/active",
                  status_code=HTTPStatus.OK,
                  response_model=GetFitnessGoalsResponse)
def get_active_goals(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetFitnessGoalsResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_active_goals(user_id=user.id)


class CompletedStatusBase(BaseModel):
    status: str


@tracking_api.patch("/goals/{goal_id}",
                    status_code=HTTPStatus.OK)
def update_fitness_goal_status(
        goal_id: str,
        request: CompletedStatusBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.update_fitness_goal_status(
        goal_id=goal_id,
        request=UpdateFitnessGoalStatusRequest(
            status=True if request.status == "completed" else False
        )
    )


@tracking_api.put("/goals/{goal_id}/progress",
                  status_code=HTTPStatus.OK,
                  response_model=FitnessGoalResponse)
def update_goal_progress(
        goal_id: str,
        current_value: float,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> FitnessGoalResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.update_goal_progress(goal_id=goal_id, user_id=user.id, current_value=current_value)


@tracking_api.get("/achievements",
                  status_code=HTTPStatus.OK,
                  response_model=GetAchievementsResponse)
def get_fitness_achievements(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetAchievementsResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_fitness_achievements(user_id=user.id)


@tracking_api.get("/summery",
                  status_code=HTTPStatus.OK,
                  response_model=GetSummeryResponse)
def get_fitness_summery(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetSummeryResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_user_fitness_summery(user_id=user.id)
