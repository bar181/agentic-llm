"""
API v1 router initialization and endpoint registration.
"""
from fastapi import APIRouter

# Create main v1 router
api_router = APIRouter()

# Import and include routes from other modules
# Example: from .endpoints import agents, tasks, graph
# api_router.include_router(agents.router, prefix="/agents", tags=["agents"])

# Export the router
__all__ = ["api_router"]
