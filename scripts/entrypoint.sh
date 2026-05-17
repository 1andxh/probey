#!/bin/bash
set -e

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting Probey API..."
exec uvicorn src:app --host 0.0.0.0 --port 8000 --workers 1