### WorkoutApp API

A FastAPI-based API for managing users, exercises, and workout plans.

### Requirements
- Python 3.11+
- pip
- Docker (optional but recommended)
- Docker Compose (optional but recommended)

### Local development (without Docker)
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Start the API:
```bash
uvicorn app.runner.asgi:app --reload
```
- The API will run at `http://127.0.0.1:8000`.
- Open API docs at `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc`.

#### Configuring SQLite database path
- By default, the app uses `workout_app.db` in the working directory.
- You can override via environment variable `DB_PATH`:
```bash
DB_PATH=/path/to/workout_app.db uvicorn app.runner.asgi:app --reload
```

### Run with Docker
1. Build the image:
```bash
docker build -t workoutapp-api .
```
2. Run the container:
```bash
docker run --rm -p 8000:8000 -e DB_PATH=/data/workout_app.db -v workout_data:/data workoutapp-api
```
- Visit `http://localhost:8000/docs`.

### Run with Docker Compose
1. Start services:
```bash
docker compose up --build
```
2. Stop services:
```bash
docker compose down
```

- The API is available at `http://localhost:8000`.
- Persistent SQLite data is stored in the named volume `workout_data`.

### Environment variables
- `DB_PATH` (string): Filesystem path to SQLite DB file. Defaults to `workout_app.db`. In Docker, default is `/data/workout_app.db`.

### Project structure
Key directories:
- `app/core`: domain logic, models, repositories, services
- `app/infra`: API routes and data persistence implementations
- `app/runner`: app bootstrap (`asgi.py`, `setup.py`)

### Seeding
On startup, a basic exercise seed runs from `app.infra.scripts.seeder`. It executes automatically in `setup()`.

### Useful commands
- Format/lint (if configured):
```bash
ruff check .
```
- Run tests (if present):
```bash
pytest -q
```

### Notes
- Hot reload is enabled by default in the Docker command and local `--reload` run.
- To customize ports, adjust `docker-compose.yml` and/or uvicorn `--port`.

