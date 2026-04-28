---
title: HarvestIQ
emoji: 🌿
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
app_port: 7860
---

# HarvestIQ 🌿

**AI-powered crop disease detection and advisory system.**

Upload a leaf photo → get instant disease diagnosis + treatment plan powered by ResNet50 + CrewAI agents.

## Features
- 🔬 ResNet50 deep learning model for disease detection
- 🤖 CrewAI agents for treatment recommendations
- 📊 GradCAM heatmap visualization
- 🗄️ PostgreSQL history tracking
- 🧠 RAG-powered knowledge base

## Tech Stack
- **Backend:** FastAPI + Python 3.11
- **ML Model:** ResNet50 (PyTorch)
- **Agents:** CrewAI + Groq LLaMA3
- **Database:** PostgreSQL (Render)
- **Vector Store:** ChromaDB
- **Frontend:** React + Vite
