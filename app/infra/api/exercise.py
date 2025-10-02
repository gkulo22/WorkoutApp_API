from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

from app.core.exercise.exceptions import GetExerciseException, ExerciseCreationException
from app.core.exercise.schemas import GetOneExerciseResponse, GetAllExercisesResponse, CreateExerciseResponse, \
    CreateExerciseRequest
from app.core.facade import PWPSCore
from app.infra.dependables import get_core



exercise_api = APIRouter()


class ExerciseBase(BaseModel):
    name: str
    exercise_code: int
    target_muscle: str
    description: str = ""
    instruction: str = ""


@exercise_api.post("",
                   status_code=HTTPStatus.CREATED,
                   response_model=CreateExerciseResponse)
def create_exercise(request: ExerciseBase,
                    core: PWPSCore = Depends(get_core)) -> CreateExerciseResponse:
    try:
        return core.create_exercise(request=CreateExerciseRequest(**request.dict()))
    except ExerciseCreationException as exc:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=exc.message)

@exercise_api.get("/{exercise_id}",
                  status_code=HTTPStatus.OK,
                  response_model=GetOneExerciseResponse)
def get_one_exercise(exercise_id: str,
                     core: PWPSCore = Depends(get_core)) -> GetOneExerciseResponse:
    try:
        return core.get_one_exercise(exercise_id=exercise_id)
    except GetExerciseException as exc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc.message)

@exercise_api.get("",
                  status_code=HTTPStatus.OK,
                  response_model=GetAllExercisesResponse)
def get_exercises(core: PWPSCore = Depends(get_core)) -> GetAllExercisesResponse:
    return core.get_all_exercises()
