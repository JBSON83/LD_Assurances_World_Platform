# Use official Python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
# (Note: We'll generate a requirements.txt if needed, but for now we install directly)
RUN pip install --no-cache-dir fastapi uvicorn gunicorn pydantic

# Copy the entire project
COPY . .

# Expose ports
# 8001 for FastAPI, 8000 for the static server (if running via python)
EXPOSE 8001
EXPOSE 8000

# Start command
# We run the backend by default. Frontend can be served by Nginx on the host or another container.
CMD ["python", "core/server.py"]
