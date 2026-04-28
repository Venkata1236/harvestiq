# HarvestIQ — HuggingFace Spaces Dockerfile
# Port 7860 is mandatory for HF Spaces

FROM python:3.11-slim

WORKDIR /app

# System dependencies for OpenCV + PostgreSQL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy React build into container (FastAPI will serve this)
COPY frontend/dist/ ./frontend/dist/

# Create persistent directories
RUN mkdir -p saved_models chroma_db

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Start FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]