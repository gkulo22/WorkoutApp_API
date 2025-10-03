from http import HTTPStatus
from typing import Optional, Annotated

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.core.exercise.exceptions import GetExerciseException
from app.core.facade import PWPSCore
from app.core.user.models import User
from app.core.workout_plan.exceptions import GetWorkoutPlanException, ExerciseNotFoundInWorkoutPlanException
from app.core.workout_plan.schemas import CreateWorkoutPlanResponse, CreateWorkoutPlanRequest, \
    GetOneWorkoutPlanResponse, \
    AddExerciseInWorkoutPlanResponse, AddCardioExerciseInWorkoutPlanRequest, AddStrengthExerciseInWorkoutPlanRequest, \
    GetAllWorkoutPlansResponse, UpdateWorkoutPlanStatusRequest
from app.infra.auth import get_current_user
from app.infra.dependables import get_core

workout_plan_api = APIRouter()
user_dependency = Annotated[User, Depends(get_current_user)]


class WorkoutPlanBase(BaseModel):
    name: str
    goal_description: str


@workout_plan_api.post("",
                       status_code=HTTPStatus.CREATED,
                       response_model=CreateWorkoutPlanResponse)
def create_workout_plan(
        request: WorkoutPlanBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> CreateWorkoutPlanResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.create_workout_plan(
        user_id=user.id,
        request=CreateWorkoutPlanRequest(**request.dict())
    )


@workout_plan_api.get("/{workout_plan_id}",
                      status_code=HTTPStatus.OK,
                      response_model=GetOneWorkoutPlanResponse)
def get_workout_plan(
        workout_plan_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)) -> GetOneWorkoutPlanResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        return core.get_one_workout_plan(user_id=user.id, workout_plan_id=workout_plan_id)
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)



@workout_plan_api.get("",
                      status_code=HTTPStatus.OK,
                      response_model=GetAllWorkoutPlansResponse)
def get_all_workout_plans(
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> GetAllWorkoutPlansResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    return core.get_all_workout_plans(user_id=user.id)


class PrivacyStatusBase(BaseModel):
    status: str



@workout_plan_api.patch("/{workout_plan_id}", status_code=HTTPStatus.OK)
def change_privacy_status(
        workout_plan_id: str,
        request: PrivacyStatusBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        return core.change_privacy_status(
            workout_plan_id=workout_plan_id,
            request=UpdateWorkoutPlanStatusRequest(
                status=True if request.status == "open" else False
            )
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)




class StrengthExerciseBase(BaseModel):
    exercise_id: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None


@workout_plan_api.post("/{workout_plan_id}/strength_exercise",
                       status_code=HTTPStatus.CREATED,
                       response_model=AddExerciseInWorkoutPlanResponse)
def add_strength_exercise_in_workout_plan(
        workout_plan_id: str,
        request: StrengthExerciseBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> AddExerciseInWorkoutPlanResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        return core.add_strength_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            user_id=user.id,
            request=AddStrengthExerciseInWorkoutPlanRequest(**request.dict()),
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))




class CardioExerciseBase(BaseModel):
    exercise_id: str
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None


@workout_plan_api.post("/{workout_plan_id}/cardio_exercise",
                       status_code=HTTPStatus.CREATED,
                       response_model=AddExerciseInWorkoutPlanResponse)
def add_cardio_exercise_in_workout_plan(
        workout_plan_id: str,
        request: CardioExerciseBase,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> AddExerciseInWorkoutPlanResponse:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        return core.add_cardio_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            user_id=user.id,
            request=AddCardioExerciseInWorkoutPlanRequest(**request.dict()),
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))





@workout_plan_api.delete("/{workout_plan_id}", status_code=HTTPStatus.OK)
def delete_workout_plan(
        workout_plan_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)
) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        core.delete_workout_plan(workout_plan_id=workout_plan_id, user_id=user.id)
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)


@workout_plan_api.delete("/{workout_plan_id}/{exercise_id}", status_code=HTTPStatus.OK)
def delete_exercise_from_workout_plan(
        workout_plan_id: str,
        exercise_id: str,
        user: user_dependency,
        core: PWPSCore = Depends(get_core)) -> None:
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authentication required")
    try:
        core.delete_exercise_from_workout_plan(
            workout_plan_id=workout_plan_id,
            user_id=user.id,
            exercise_id=exercise_id
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except ExerciseNotFoundInWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)