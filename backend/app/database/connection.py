from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# ─── Base Class ───────────────────────────────────────────────────────────────
# All database models inherit from this
class Base(DeclarativeBase):
    pass


# ─── Engine ───────────────────────────────────────────────────────────────────
# create_async_engine → non-blocking DB calls
# pool_pre_ping=True  → auto-reconnect if connection drops
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENV == "development",  # logs SQL queries in dev only
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


# ─── Session Factory ──────────────────────────────────────────────────────────
# AsyncSessionLocal() creates a new DB session per request
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # keeps objects accessible after commit
    autocommit=False,
    autoflush=False,
)


# ─── Dependency ───────────────────────────────────────────────────────────────
async def get_db() -> AsyncSession:
    """
    FastAPI dependency — injects DB session into route handlers.
    Automatically commits on success, rolls back on exception.

    Usage in routes:
        async def my_route(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise


# ─── Table Creation ───────────────────────────────────────────────────────────
async def create_tables() -> None:
    """
    Creates all tables defined in models.py if they don't exist.
    Called once at FastAPI startup via lifespan.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified")