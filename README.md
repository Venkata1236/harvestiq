"""# 🌾 HarvestIQ

> AI-powered crop disease detection — ResNet50 + RAG + FastAPI + React

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![PyTorch](https://img.shields.io/badge/PyTorch-ResNet50-orange)
![React](https://img.shields.io/badge/React-Vite-cyan)
![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-purple)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-yellow)

---

## 📌 What Is This?

An end-to-end AI system that detects crop diseases from leaf images with 82%+ confidence. Upload a photo → ResNet50 classifies the disease → RAG retrieves knowledge → AI agents generate diagnosis + treatment advice → saved to PostgreSQL.

---

## 🗺️ Simple Flow
```
User uploads leaf image
        ↓
React frontend → POST /api/detect
        ↓
ResNet50 classifies disease (38 classes)
        ↓
ChromaDB RAG retrieves disease knowledge
        ↓
AI Agents → Diagnosis + Treatment advice
        ↓
Saved to PostgreSQL → Response to UI
```

---

## 📁 Project Structure
```
harvestiq/
├── backend/
│   ├── app/
│   │   ├── main.py                  ← FastAPI app + lifespan
│   │   ├── routes/
│   │   │   └── detect.py            ← POST /api/detect endpoint
│   │   ├── ml/
│   │   │   ├── model.py             ← ResNet50 inference
│   │   │   └── preprocess.py        ← Image preprocessing
│   │   ├── rag/
│   │   │   └── retriever.py         ← ChromaDB knowledge retrieval
│   │   ├── agents/
│   │   │   ├── disease_analyst.py   ← AI diagnosis agent
│   │   │   └── treatment_advisor.py ← AI treatment agent
│   │   └── database/
│   │       └── connection.py        ← PostgreSQL setup
│   ├── saved_models/
│   │   └── harvestiq_resnet50.pt    ← Trained model (LFS)
│   ├── chroma_db/                   ← Vector store
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Upload.tsx           ← Image upload page
│   │   │   ├── Results.tsx          ← Detection results page
│   │   │   └── History.tsx          ← Detection history page
│   │   └── services/
│   │       └── api.ts               ← Axios API client
│   ├── index.html
│   └── vite.config.ts
└── README.md
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/detect` | Upload image → disease detection |
| GET | `/api/detections` | Get all detection history |
| GET | `/api/detections/{id}` | Get single detection |
| DELETE | `/api/detections/{id}` | Delete a detection |

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| `ResNet50` | Classifies 38 crop disease classes from leaf images |
| `ChromaDB RAG` | Retrieves disease-specific knowledge for context |
| `AI Agents` | Generate diagnosis summary + treatment advice |
| `PostgreSQL` | Persists all detections with metadata |
| `React + Vite` | Frontend served statically by FastAPI |

---

## 🌿 Supported Crops & Diseases

38 classes across crops including Tomato, Potato, Corn, Apple, Grape, Pepper, Strawberry, Peach, Cherry, and more — covering diseases like Late Blight, Early Blight, Leaf Mold, Black Rot, and healthy states.

---

## ⚙️ Local Setup

```bash
cd backend
pip install -r requirements.txt
```

Add `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/harvestiq
OPENAI_API_KEY=your_key_here
```

Run:
```bash
# Backend
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

---

## 🚀 Deployment

Live on Hugging Face Spaces (Docker):
**[https://venkat1236-harvestiq.hf.space](https://venkat1236-harvestiq.hf.space)**

- FastAPI serves React build as static files
- PostgreSQL via Hugging Face datasets
- ResNet50 model stored via Git LFS

---

## 📦 Tech Stack

- **FastAPI** — REST API + static file serving
- **PyTorch + ResNet50** — Crop disease classification
- **ChromaDB** — Vector store for RAG knowledge retrieval
- **PostgreSQL** — Detection history storage
- **React + Vite + TypeScript** — Frontend UI
- **Docker** — Single container deployment

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)
"""