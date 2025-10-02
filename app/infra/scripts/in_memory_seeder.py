from typing import List

from app.core.exercise import Muscle
from app.core.exercise.models import Exercise
from app.core.exercise.repository import IExerciseRepository

REAL_EXERCISES = [
    ("Push-Up", Muscle.CHEST, "Do push-ups", "Keep your back straight"),
    ("Bench Press", Muscle.CHEST, "Bench press with barbell", "Lower bar slowly"),
    ("Pull-Up", Muscle.BACK, "Pull your body up", "Engage lats"),
    ("Lat Pulldown", Muscle.LATS, "Use machine to pull bar down", "Control the motion"),
    ("Shoulder Press", Muscle.SHOULDERS, "Press dumbbells overhead", "Avoid arching back"),
    ("Lateral Raise", Muscle.SHOULDERS, "Raise dumbbells to sides", "Slight bend in elbows"),
    ("Bicep Curl", Muscle.BICEPS, "Curl dumbbells", "Keep elbows fixed"),
    ("Hammer Curl", Muscle.BICEPS, "Curl dumbbells neutral grip", "Focus on forearms too"),
    ("Tricep Dip", Muscle.TRICEPS, "Dip on parallel bars", "Keep elbows tight"),
    ("Tricep Pushdown", Muscle.TRICEPS, "Push cable down", "Control the weight"),
    ("Plank", Muscle.CORE, "Hold plank position", "Keep back straight"),
    ("Russian Twist", Muscle.OBLIQUES, "Twist torso with weight", "Feet off floor optional"),
    ("Crunches", Muscle.ABS, "Classic crunch", "Do controlled reps"),
    ("Squat", Muscle.QUADS, "Bodyweight or barbell squat", "Keep knees aligned"),
    ("Lunge", Muscle.QUADS, "Step forward into lunge", "Keep torso upright"),
    ("Deadlift", Muscle.HAMSTRINGS, "Lift barbell from floor", "Engage hamstrings and back"),
    ("Glute Bridge", Muscle.GLUTES, "Lift hips off floor", "Squeeze glutes at top"),
    ("Calf Raise", Muscle.CALVES, "Raise heels off floor", "Slow controlled movement"),
    ("Shrugs", Muscle.TRAPS, "Lift shoulders with dumbbells", "Don't rotate neck"),
    ("Face Pull", Muscle.TRAPS, "Pull rope towards face", "Keep elbows high")
]

def seed_real_exercises(repo: IExerciseRepository) -> List[Exercise]:
    exercises = []
    used_codes = set()

    for i, (name, muscle, description, instruction) in enumerate(REAL_EXERCISES):
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