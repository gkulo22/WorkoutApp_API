import sqlite3

from fastapi import FastAPI

from app.core.facade import PWPSCore
from app.infra.api.auth import auth_api
from app.infra.api.exercise import exercise_api
from app.infra.api.workout_plan import workout_plan_api
from app.infra.data.in_memory import InMemoryRepoFactory
from app.infra.data.sqlite import SqliteRepoFactory
from app.infra.scripts.in_memory_seeder import seed_real_exercises


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_api, prefix="/auth", tags=["Auth"])
    app.include_router(exercise_api, prefix="/exercise", tags=["Exercise"])
    app.include_router(workout_plan_api, prefix="/workout_plan", tags=["Workout Plan"])

    # connection = sqlite3.connect("workout_app.db", check_same_thread=False)
    # database = SqliteRepoFactory(connection=connection)
    database = InMemoryRepoFactory()
    seed_real_exercises(database.exercises())
    app.state.infra = database
    app.state.core = PWPSCore.create(database)

    return app