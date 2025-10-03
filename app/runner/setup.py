import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI

from app.core.facade import PWPSCore
from app.infra.api.auth import auth_api
from app.infra.api.exercise import exercise_api
from app.infra.api.tracking import tracking_api
from app.infra.api.workout_plan import workout_plan_api
from app.infra.api.workout_session import workout_session_api
from app.infra.data.in_memory import InMemoryRepoFactory
from app.infra.data.sqlite import SqliteRepoFactory
from app.infra.scripts.seeder import seed_exercises


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(auth_api, prefix="/auth", tags=["Auth"])
    app.include_router(exercise_api, prefix="/exercise", tags=["Exercise"])
    app.include_router(workout_plan_api, prefix="/workout_plan", tags=["Workout Plan"])
    app.include_router(workout_session_api, prefix="/workout_session", tags=["Workout Session"])
    app.include_router(tracking_api, prefix="/tracking", tags=["Tracking and Goals"])

    db_path = os.getenv("DB_PATH", "workout_app.db")
    db_file = Path(db_path)
    if db_file.parent and not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_file), check_same_thread=False)
    database = SqliteRepoFactory(connection=connection)
    # database = InMemoryRepoFactory()
    seed_exercises(database.exercises())
    app.state.infra = database
    app.state.core = PWPSCore.create(database)

    return app