# HarvestIQ — HuggingFace Spaces Dockerfile
# Port 7860 is mandatory for HF Spaces

FROM python:3.11-slim

WORKDIR /app

# System dependencies for OpenCV + PostgreSQL (Debian Trixie compatible)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies in two stages to avoid crewai/chromadb conflict:
# crewai==0.67.1 pulls embedchain which conflicts with chromadb>=0.5.x
# Fix: install everything except crewai first, then crewai --no-deps
COPY backend/requirements.txt .
RUN grep -v "^crewai" requirements.txt > /tmp/requirements_base.txt && \
    pip install --no-cache-dir -r /tmp/requirements_base.txt && \
    pip install --no-cache-dir --no-deps crewai==0.67.1

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