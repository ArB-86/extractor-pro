from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(
    title="ShikshaVault API",
    version="1.0.0",
    description="Production API for ShikshaVault powered by Extractor-Pro",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["System"])
async def root():
    return {
        "name": "ShikshaVault",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health", tags=["System"])
async def health():
    return {"status": "healthy"}
