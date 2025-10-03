from typing import List

from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository
from app.infra.scripts import EXERCISES


def seed_exercises(repo: IExerciseRepository) -> List[Exercise]:
    exercises = repo.get_all()
    if len(exercises) > 0:
        return exercises
    used_codes = set()

    for i, (name, muscle, description, instruction) in enumerate(EXERCISES):
        while True:
            code = 1000 + i
            if code not in used_codes:
                used_codes.add(code)
                break

        exercise = Exercise(
            id="",
            name=name,
            exercise_code=code,
            target_muscle=muscle,
            description=description,
            instruction=instruction
        )
        repo.create(exercise)
        exercises.append(exercise)

    return exercises