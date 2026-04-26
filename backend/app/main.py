from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.database.connection import create_tables
from app.ml.model import model_manager
from app.routes.detect import router as detect_router


# ─── Lifespan ─────────────────────────────────────────────────────────────────
# Runs ONCE at startup and ONCE at shutdown
# This is where we load the model and create DB tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──────────────────────────────────────────────────────────────
    logger.info("HarvestIQ API starting up...")

    # Create DB tables if they don't exist
    try:
        await create_tables()
        logger.info("Database ready")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.warning("Continuing without database — detections won't be saved")

    # Load ML model into memory
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

    # ── SHUTDOWN ──────────────────────────────────────────────────────────────
    logger.info("HarvestIQ API shutting down...")


# ─── App Instance ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="HarvestIQ API",
    description=(
        "Production-grade crop disease detection and advisory system. "
        "Upload a leaf photo → get disease diagnosis + treatment plan."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
)


# ─── CORS ─────────────────────────────────────────────────────────────────────
# Allows React frontend (localhost:5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # React dev server
        "http://localhost:3000",    # Alternative React port
        "https://harvestiq.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Routes ───────────────────────────────────────────────────────────────────
app.include_router(detect_router)
# Day 2: app.include_router(advisory_router)


# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "project": "HarvestIQ",
        "description": "Crop disease detection and advisory system",
        "docs": "/docs",
        "health": "/api/health",
        "version": "1.0.0"
    }


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENV == "development",
        log_level=settings.LOG_LEVEL.lower()
    )