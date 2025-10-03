### WorkoutApp API Reference

Base URL: `http://localhost:8000`

Authentication
- Scheme: OAuth2 password flow with Bearer token
- Token endpoint: `POST /auth/token` (form fields `username`, `password`)
- Use header: `Authorization: Bearer <token>` for protected endpoints

---

## Auth

POST /auth
- Create a new user
- Body:
```json
{ "username": "string", "password": "string" }
```
- Responses: 201 Created (no body)

POST /auth/token
- Obtain access token
- Form data (application/x-www-form-urlencoded): `username`, `password`
- Response 200:
```json
{ "access_token": "string", "token_type": "bearer" }
```

---

## Exercise

POST /exercise
- Create exercise
- Body:
```json
{
  "name": "string",
  "exercise_code": 0,
  "target_muscle": "Chest",
  "description": "string",
  "instruction": "string"
}
```
- Response 201:
```json
{ "exercise": { "id": "string", "name": "string", "exercise_code": 0, "target_muscle": "Chest", "description": "", "instruction": "" } }
```

GET /exercise/{exercise_id}
- Get one exercise
- Response 200:
```json
{ "name": "string", "exercise_code": 0, "target_muscle": "Chest", "description": "", "instruction": "" }
```

GET /exercise
- List all exercises
- Response 200:
```json
{ "exercises": [ { "id": "string", "name": "string", "exercise_code": 0, "target_muscle": "Chest", "description": "", "instruction": "" } ] }
```

---

## Workout Plan (protected)
All endpoints require `Authorization: Bearer <token>`.

POST /workout_plan
- Create a workout plan
- Body:
```json
{ "name": "string", "goal_description": "string" }
```
- Response 201:
```json
{ "id": "string", "name": "string", "exercises": [], "goal_description": "string" }
```

GET /workout_plan/{workout_plan_id}
- Get one workout plan
- Response 200 like create response

GET /workout_plan
- List workout plans for current user
- Response 200:
```json
{ "workout_plans": [ { "id": "string", "author_id": "string", "name": "string", "exercises": [], "goal_description": "string" } ] }
```

PATCH /workout_plan/{workout_plan_id}
- Change privacy status
- Body:
```json
{ "status": "open" | "closed" }
```
- Response 200 (no body)

POST /workout_plan/{workout_plan_id}/strength_exercise
- Add strength exercise to plan
- Body:
```json
{ "exercise_id": "string", "sets": 3, "reps": 10, "weight": 50 }
```
- Response 201: workout plan object like create response

POST /workout_plan/{workout_plan_id}/cardio_exercise
- Add cardio exercise to plan
- Body:
```json
{ "exercise_id": "string", "duration": 30, "distance": 5, "calories": 300 }
```
- Response 201: workout plan object like create response

DELETE /workout_plan/{workout_plan_id}
- Delete plan
- Response 200 (no body)

DELETE /workout_plan/{workout_plan_id}/{exercise_id}
- Remove exercise from plan
- Response 200 (no body)

---

## Workout Session (protected)
Note: Schemas are placeholders in code; responses are subject to change.

POST /workout_session/start/{workout_id}
- Start a session for a workout
- Response 201: `{}` (until implemented)

POST /workout_session/{session_id}/complete
- Complete current session
- Response 200: `{}` (until implemented)

GET /workout_session/{session_id}
- Get session details
- Response 200: `{}` (until implemented)

PUT /workout_session/{session_id}/exercise/{exercise_id}/progress
- Update progression for an exercise in session
- Body: `{}` (until implemented)
- Response 200: `{}` (until implemented)

POST /workout_session/{session_id}/exercise/next
- Move to next exercise in session
- Response 200: `{}` (until implemented)

---

## Tracking and Goals (protected)

GET /tracking/weight
- Get weight history
- Response 200:
```json
{ "entries": [] }
```

POST /tracking/weight
- Record weight
- Body: `{}` (fields TBD in core schema)
- Response 201:
```json
{ }
```

GET /tracking/weight/latest
- Latest weight entry
- Response 200: `{ }`

DELETE /tracking/weight/{entry_id}
- Delete weight entry
- Response 200 (no body)

GET /tracking/goals
- List goals
- Response 200: `{ }`

POST /tracking/goals
- Create goal
- Body: `{}`
- Response 201: `{}`

PUT /tracking/goals/{goal_id}
- Update goal details
- Body: `{}`
- Response 200: `{}`

DELETE /tracking/goals/{goal_id}
- Delete a goal
- Response 200 (no body)

GET /tracking/goals/active
- List active goals
- Response 200: `{}`

PATCH /tracking/goals/{goal_id}
- Update goal status
- Body:
```json
{ "status": "completed" | "in_progress" }
```
- Response 200 (no body)

PUT /tracking/goals/{goal_id}/progress?current_value=number
- Update progress value
- Response 200: `{}`

GET /tracking/achievements
- Get achievements
- Response 200: `{}`

GET /tracking/summery
- Summary
- Response 200: `{}`

---

### Quickstart (local)
1) Start server: `uvicorn app.runner.asgi:app --reload`
2) Create a user:
```bash
curl -X POST http://localhost:8000/auth -H "Content-Type: application/json" -d '{"username":"u","password":"p"}'
```
3) Get token:
```bash
curl -X POST http://localhost:8000/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=u&password=p"
```
4) Use token:
```bash
TOKEN=...; curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/exercise
```

OpenAPI UIs: `/docs` (Swagger), `/redoc`.


