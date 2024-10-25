"""
Database models for agents in the system.
"""
from sqlalchemy import Column, Integer, String, Float, JSON, Enum, DateTime
from sqlalchemy.sql import func
import enum

from ...db.base import Base

class AgentStatus(enum.Enum):
    """Status states for agents"""
    IDLE = "idle"
    ACTIVE = "active"
    LEARNING = "learning"
    SUSPENDED = "suspended"
    ERROR = "error"

class AgentType(enum.Enum):
    """Types of agents in the system"""
    LOCAL = "local"
    CONTROLLER = "controller"
    SPECIALIST = "specialist"

class Agent(Base):
    """
    Database model for AI agents in the system.
    """
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(Enum(AgentType))
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE)
    version = Column(String)
    capabilities = Column(JSON)  # List of agent capabilities/skills
    performance_metrics = Column(JSON)  # Historical performance data
    memory_usage = Column(Float)  # Current memory usage in MB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Configuration for the agent
    config = Column(JSON)
    
    # Learning parameters and state
    learning_state = Column(JSON)
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.type.value})>"
        
    def transition_status(self, new_status: AgentStatus) -> bool:
        """
        Safely transition agent status with validation
        Returns True if transition was successful
        """
        valid_transitions = {
            AgentStatus.IDLE: [AgentStatus.ACTIVE, AgentStatus.LEARNING],
            AgentStatus.ACTIVE: [AgentStatus.IDLE, AgentStatus.SUSPENDED, AgentStatus.ERROR],
            AgentStatus.LEARNING: [AgentStatus.IDLE, AgentStatus.ERROR],
            AgentStatus.SUSPENDED: [AgentStatus.IDLE, AgentStatus.ERROR],
            AgentStatus.ERROR: [AgentStatus.IDLE]
        }
        
        if new_status in valid_transitions.get(self.status, []):
            self.status = new_status
            return True
        return False
