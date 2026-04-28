import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.core.config import settings
from app.database.connection import create_tables
from app.ml.model import model_manager
from app.routes.detect import router as detect_router
from app.routes.history import router as history_router

# ─── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ────────────────────────────────────────────────────────────────
    logger.info("HarvestIQ API starting up...")

    try:
        await create_tables()
        logger.info("Database ready")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.warning("Continuing without database — detections won't be saved")

    try:
        model_manager.load()
        if model_manager.is_loaded:
            logger.info(
                f"Model ready | "
                f"Classes: {len(model_manager.class_names)} | "
                f"Device: {model_manager.device}"
            )
        else:
            logger.warning(
                "Model not loaded — train on Colab first. "
                "Place harvestiq_resnet50.pt in backend/saved_models/"
            )
    except Exception as e:
        logger.error(f"Model loading failed: {e}")

    logger.info(f"HarvestIQ API ready | ENV={settings.ENV}")

    yield  # App runs here

    # ── SHUTDOWN ───────────────────────────────────────────────────────────────
    logger.info("HarvestIQ API shutting down...")


# ─── App Instance ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="HarvestIQ API",
    description=(
        "Production-grade crop disease detection and advisory system. "
        "Upload a leaf photo → get disease diagnosis + treatment plan."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://harvestiq.vercel.app",
        "https://venkata1236-harvestiq.hf.space",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Routes ────────────────────────────────────────────────────────────────────
app.include_router(detect_router, prefix="/api", tags=["Detection"])
app.include_router(history_router, prefix="/api", tags=["History"])


# ─── Root ──────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/health", tags=["Health"])
async def api_health():
    return {
        "status": "ok",
        "model_loaded": model_manager.is_loaded,
        "version": "1.0.0"
    }


# ─── Serve React Frontend ──────────────────────────────────────────────────────
# Must be LAST — catches all non-API routes and serves React
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


# ─── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=7860,
        reload=settings.ENV == "development",
        log_level=settings.LOG_LEVEL.lower()
    )