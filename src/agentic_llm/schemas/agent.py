"""
Pydantic schemas for agent-related operations.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    LEARNING = "learning"
    SUSPENDED = "suspended"
    ERROR = "error"

class AgentType(str, Enum):
    LOCAL = "local"
    CONTROLLER = "controller"
    SPECIALIST = "specialist"

class AgentBase(BaseModel):
    """Base schema for agent data"""
    name: str = Field(..., description="Unique name of the agent")
    type: AgentType
    capabilities: List[str] = Field(default_factory=list, description="List of agent capabilities")
    config: Dict = Field(default_factory=dict, description="Agent configuration parameters")

class AgentCreate(AgentBase):
    """Schema for creating a new agent"""
    pass

class AgentUpdate(BaseModel):
    """Schema for updating an existing agent"""
    name: Optional[str] = None
    status: Optional[AgentStatus] = None
    capabilities: Optional[List[str]] = None
    config: Optional[Dict] = None
    performance_metrics: Optional[Dict] = None
    memory_usage: Optional[float] = None
    learning_state: Optional[Dict] = None

class AgentInDB(AgentBase):
    """Schema for agent data as stored in database"""
    id: int
    status: AgentStatus
    version: str
    performance_metrics: Dict
    memory_usage: float
    created_at: datetime
    updated_at: Optional[datetime]
    learning_state: Dict

    class Config:
        orm_mode = True

class AgentResponse(AgentInDB):
    """Schema for agent responses to API requests"""
    pass
