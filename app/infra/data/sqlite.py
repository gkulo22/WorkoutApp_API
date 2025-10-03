import sqlite3
import uuid
from dataclasses import dataclass
from typing import Optional, List

from app.core.exercise import Muscle
from app.core.exercise.models import Exercise, StrengthExercise, CardioExercise
from app.core.exercise.repository import IExerciseRepository
from app.core.factories.repo_factory import RepoFactory
from app.core.user.models import User
from app.core.user.repository import IUserRepository
from app.core.workout_plan.models import WorkoutPlan
from app.core.workout_plan.repository import IWorkoutPlanRepository



@dataclass
class UserSqliteRepository(IUserRepository):
    connection: sqlite3.Connection

    def create(self, user: User) -> User:
        user_id = str(uuid.uuid4())
        setattr(user, "id", user_id)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (id, username, hashed_password)
            VALUES (?, ?, ?)
            """,
            (user.id, user.username, user.hashed_password)
        )
        self.connection.commit()
        return user

    def get_user(self, username: str) -> Optional[User]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, username, hashed_password FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return User(id=row[0], username=row[1], hashed_password=row[2])

    def username_exists(self, username: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? LIMIT 1",
            (username,)
        )
        return cursor.fetchone() is not None


@dataclass
class ExerciseSqliteRepository(IExerciseRepository):
    connection: sqlite3.Connection

    def create(self, exercise: Exercise) -> Exercise:
        exercise_id = str(uuid.uuid4())
        setattr(exercise, "id", exercise_id)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO exercises (
                id, name, exercise_code, target_muscle, description, instruction
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                exercise.id,
                exercise.name,
                exercise.exercise_code,
                exercise.target_muscle.value,
                exercise.description,
                exercise.instruction,
            )
        )
        self.connection.commit()
        return exercise

    def get_one(self, exercise_id: str) -> Optional[Exercise]:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT id, name, exercise_code, target_muscle, description, instruction
            FROM exercises WHERE id = ?
            """,
            (exercise_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Exercise(
            id=row[0],
            name=row[1],
            exercise_code=row[2],
            target_muscle=Muscle(row[3]),
            description=row[4] or "",
            instruction=row[5] or "",
        )

    def get_all(self) -> List[Exercise]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, name, exercise_code, target_muscle, description, instruction FROM exercises"
        )
        exercises: List[Exercise] = []
        for row in cursor.fetchall():
            exercises.append(
                Exercise(
                    id=row[0],
                    name=row[1],
                    exercise_code=row[2],
                    target_muscle=Muscle(row[3]),
                    description=row[4] or "",
                    instruction=row[5] or "",
                )
            )
        return exercises

    def has_code(self, exercise_code: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT 1 FROM exercises WHERE exercise_code = ? LIMIT 1",
            (exercise_code,)
        )
        return cursor.fetchone() is not None



@dataclass
class WorkoutPlanSqliteRepository(IWorkoutPlanRepository):
    connection: sqlite3.Connection

    def create(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        workout_plan_id = str(uuid.uuid4())
        setattr(workout_plan, "id", workout_plan_id)
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO workout_plans (id, author_id, name, goal_description)
            VALUES (?, ?, ?, ?)
            """,
            (
                workout_plan.id,
                workout_plan.author_id,
                workout_plan.name,
                workout_plan.goal_description,
            )
        )
        # Persist exercises list if any
        for ex in workout_plan.exercises:
            self._upsert_exercise(cursor, workout_plan.id, ex)
        self.connection.commit()
        return workout_plan

    def get_one(self, workout_plan_id: str) -> Optional[WorkoutPlan]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, author_id, name, goal_description FROM workout_plans WHERE id = ?",
            (workout_plan_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None

        exercises = self._load_exercises(cursor, workout_plan_id)
        return WorkoutPlan(
            id=row[0],
            author_id=row[1],
            name=row[2],
            exercises=exercises,
            goal_description=row[3] or "",
        )

    def get_all(self, author_id: str) -> List[WorkoutPlan]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, author_id, name, goal_description FROM workout_plans WHERE author_id = ?",
            (author_id,)
        )
        result: List[WorkoutPlan] = []
        rows = cursor.fetchall()
        for row in rows:
            wp_id = row[0]
            exercises = self._load_exercises(cursor, wp_id)
            result.append(
                WorkoutPlan(
                    id=wp_id,
                    author_id=row[1],
                    name=row[2],
                    exercises=exercises,
                    goal_description=row[3] or "",
                )
            )
        return result

    def delete(self, workout_plan_id: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM workout_plan_exercises WHERE workout_plan_id = ?",
            (workout_plan_id,)
        )
        cursor.execute(
            "DELETE FROM workout_plans WHERE id = ?",
            (workout_plan_id,)
        )
        self.connection.commit()

    def add_exercise(self, workout_plan: WorkoutPlan) -> WorkoutPlan:
        cursor = self.connection.cursor()
        # Strategy mirrors in-memory behavior: replace current state with provided
        cursor.execute(
            "DELETE FROM workout_plan_exercises WHERE workout_plan_id = ?",
            (workout_plan.id,)
        )
        for ex in workout_plan.exercises:
            self._upsert_exercise(cursor, workout_plan.id, ex)
        self.connection.commit()
        return workout_plan

    def delete_exercise(self, workout_plan: WorkoutPlan) -> None:
        # Same behavior as in-memory: overwrite with provided state
        self.add_exercise(workout_plan)

    # Internal helpers
    def _upsert_exercise(self, cursor: sqlite3.Cursor, workout_plan_id: str, ex: object) -> None:
        if isinstance(ex, StrengthExercise):
            cursor.execute(
                """
                INSERT INTO workout_plan_exercises (
                    id, workout_plan_id, exercise_id, exercise_type, sets, reps, weight,
                    duration, distance, calories
                ) VALUES (?, ?, ?, 'strength', ?, ?, ?, NULL, NULL, NULL)
                """,
                (
                    ex.id,
                    workout_plan_id,
                    ex.id,
                    ex.sets,
                    ex.reps,
                    ex.weight,
                )
            )
        elif isinstance(ex, CardioExercise):
            cursor.execute(
                """
                INSERT INTO workout_plan_exercises (
                    id, workout_plan_id, exercise_id, exercise_type, sets, reps, weight,
                    duration, distance, calories
                ) VALUES (?, ?, ?, 'cardio', NULL, NULL, NULL, ?, ?, ?)
                """,
                (
                    ex.id,
                    workout_plan_id,
                    ex.id,
                    ex.duration,
                    ex.distance,
                    ex.calories,
                )
            )
        else:
            # Fallback: ignore unknown item types silently
            pass

    def _load_exercises(self, cursor: sqlite3.Cursor, workout_plan_id: str) -> List[object]:
        cursor.execute(
            """
            SELECT exercise_type, exercise_id, sets, reps, weight, duration, distance, calories
            FROM workout_plan_exercises
            WHERE workout_plan_id = ?
            """,
            (workout_plan_id,)
        )
        exercises: List[object] = []
        for row in cursor.fetchall():
            ex_type = row[0]
            if ex_type == "strength":
                exercises.append(
                    StrengthExercise(
                        id=row[1],
                        sets=row[2],
                        reps=row[3],
                        weight=row[4],
                    )
                )
            elif ex_type == "cardio":
                exercises.append(
                    CardioExercise(
                        id=row[1],
                        duration=row[5],
                        distance=row[6],
                        calories=row[7],
                    )
                )
        return exercises




@dataclass
class SqliteRepoFactory(RepoFactory):
    connection: sqlite3.Connection

    def __post_init__(self) -> None:
        self._initialize_db()

    def _initialize_db(self) -> None:
        cursor = self.connection.cursor()

        # Users
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
            """
        )

        # Exercises
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                exercise_code INTEGER NOT NULL UNIQUE,
                target_muscle TEXT NOT NULL,
                description TEXT,
                instruction TEXT
            )
            """
        )

        # Workout plans
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_plans (
                id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL,
                name TEXT NOT NULL,
                goal_description TEXT
            )
            """
        )

        # Workout plan exercises
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workout_plan_exercises (
                id TEXT PRIMARY KEY,
                workout_plan_id TEXT NOT NULL,
                exercise_id TEXT NOT NULL,
                exercise_type TEXT NOT NULL,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                duration REAL,
                distance REAL,
                calories REAL,
                FOREIGN KEY (workout_plan_id) REFERENCES workout_plans (id)
            )
            """
        )

        self.connection.commit()

    def users(self) -> IUserRepository:
        return UserSqliteRepository(self.connection)

    def exercises(self) -> IExerciseRepository:
        return ExerciseSqliteRepository(self.connection)

    def workout_plans(self) -> IWorkoutPlanRepository:
        return WorkoutPlanSqliteRepository(self.connection)
