from apexdevkit.fastapi import router
from fastapi import FastAPI

from app.core.facade import PWPSCore
from app.infra.api.exercise import exercise_api
from app.infra.data.in_memory import InMemoryRepoFactory


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(exercise_api, prefix="/exercise", tags=["Exercise"])

    database = InMemoryRepoFactory()
    app.state.infra = database
    app.state.core = PWPSCore.create(database)

    return app