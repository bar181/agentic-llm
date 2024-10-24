"""
Configuration settings for the Agentic LLM application.
"""
from pydantic import BaseSettings
from typing import Optional, Dict, Any
import os

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agentic LLM"
    
    # Database Settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./agentic_llm.db"
    )
    
    # Security Settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-secret-key-here-please-change-in-production"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Agent Settings
    MAX_AGENTS: int = 100
    AGENT_MEMORY_LIMIT: int = 1000  # MB
    
    # Graph Repository Settings
    GRAPH_DB_URL: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Global instance
settings = Settings()
