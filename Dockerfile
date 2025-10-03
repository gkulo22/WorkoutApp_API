FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first (better caching)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Default envs
ENV DB_PATH=/data/workout_app.db

# Create data dir
RUN mkdir -p /data
VOLUME ["/data"]

EXPOSE 8000

CMD ["uvicorn", "app.runner.asgi:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

