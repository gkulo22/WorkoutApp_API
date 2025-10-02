from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from app.core.exercise.exceptions import GetExerciseException
from app.core.facade import PWPSCore
from app.core.workout.exceptions import GetWorkoutPlanException, ExerciseNotFoundInWorkoutPlanException
from app.core.workout.schemas import CreateWorkoutPlanResponse, CreateWorkoutPlanRequest, GetOneWorkoutPlanResponse, \
    AddExerciseInWorkoutPlanResponse, AddCardioExerciseInWorkoutPlanRequest, AddStrengthExerciseInWorkoutPlanRequest
from app.infra.dependables import get_core

workout_plan_api = APIRouter()


class WorkoutPlanBase(BaseModel):
    name: str
    goal_description: str


@workout_plan_api.post("",
                       status_code=HTTPStatus.CREATED,
                       response_model=CreateWorkoutPlanResponse)
def create_workout_plan(request: WorkoutPlanBase,
                        core: PWPSCore = Depends(get_core)) -> CreateWorkoutPlanResponse:
    return core.create_workout_plan(request=CreateWorkoutPlanRequest(**request.dict()))


@workout_plan_api.get("/{workout_plan_id}",
                      status_code=HTTPStatus.OK,
                      response_model=GetOneWorkoutPlanResponse)
def get_workout_plan(workout_plan_id: str, core: PWPSCore = Depends(get_core)) -> GetOneWorkoutPlanResponse:
    try:
        return core.get_one_workout_plan(workout_plan_id=workout_plan_id)
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)





class StrengthExerciseBase(BaseModel):
    id: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None


@workout_plan_api.post("/{workout_plan_id}/strength_exercise",
                       status_code=HTTPStatus.CREATED,
                       response_model=AddStrengthExerciseInWorkoutPlanRequest)
def add_strength_exercise_in_workout_plan(
        workout_plan_id: str,
        strength_exercise: StrengthExerciseBase,
        core: PWPSCore = Depends(get_core)
) -> AddExerciseInWorkoutPlanResponse:
    try:
        return core.add_strength_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            request=AddStrengthExerciseInWorkoutPlanRequest(**strength_exercise.dict()),
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)




class CardioExerciseBase(BaseModel):
    id: str
    duration: Optional[float] = None
    distance: Optional[float] = None
    calories: Optional[float] = None


@workout_plan_api.post("/{workout_plan_id}/cardio_exercise",
                       status_code=HTTPStatus.CREATED,
                       response_model=AddCardioExerciseInWorkoutPlanRequest)
def add_cardio_exercise_in_workout_plan(
        workout_plan_id: str,
        cardio_exercise: CardioExerciseBase,
        core: PWPSCore = Depends(get_core)
) -> AddExerciseInWorkoutPlanResponse:
    if cardio_exercise.duration is not None and cardio_exercise.duration < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid quantity")

    if cardio_exercise.distance is not None and cardio_exercise.distance < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid quantity")

    if cardio_exercise.calories is not None and cardio_exercise.calories < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid quantity")

    try:
        return core.add_cardio_exercise_in_workout_plan(
            workout_plan_id=workout_plan_id,
            request=AddCardioExerciseInWorkoutPlanRequest(**cardio_exercise.dict()),
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)





@workout_plan_api.delete("/{workout_plan_id}", status_code=HTTPStatus.OK)
def delete_workout_plan(workout_plan_id: str, core: PWPSCore = Depends(get_core)) -> None:
    try:
        core.delete_workout_plan(workout_plan_id=workout_plan_id)
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)


@workout_plan_api.delete("/{workout_plan_id}/{exercise_id}", status_code=HTTPStatus.OK)
def delete_exercise_from_workout_plan(
        workout_plan_id: str,
        exercise_id: str,
        core: PWPSCore = Depends(get_core)) -> None:
    try:
        core.delete_exercise_from_workout_plan(
            workout_plan_id=workout_plan_id,
            exercise_id=exercise_id
        )
    except GetWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)
    except ExerciseNotFoundInWorkoutPlanException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)