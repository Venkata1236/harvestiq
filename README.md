# HarvestIQ

Production-grade crop disease detection and advisory system for Indian farmers.

Farmer photographs a leaf -> ResNet50 identifies the disease -> CrewAI advisory crew delivers a complete crop rescue plan in 30 seconds.

## Stack
- CV: ResNet50 (PyTorch) + Grad-CAM explainability
- Agents: CrewAI 3-agent sequential crew
- RAG: ChromaDB + sentence-transformers
- Backend: FastAPI async + PostgreSQL
- Frontend: React + Vite + TailwindCSS
- Infra: Docker + K8s Ingress + HuggingFace Spaces

## Setup
cp backend/.env.example backend/.env
docker-compose up --build

## Live Demo
Coming soon
