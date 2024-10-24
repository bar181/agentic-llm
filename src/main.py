"""
Main application entry point for Agentic LLM.
"""
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from logging.config import dictConfig

# Configure logging
dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
})

logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware

from agentic_llm.core.config import settings
from agentic_llm.api.v1 import api_router
from agentic_llm.db.base import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events handler"""
    # Startup
    logger.info("Starting Agentic LLM API")
    yield
    # Shutdown
    logger.info("Shutting down Agentic LLM API")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Agentic LLM API",
        "version": "0.1.0",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
