"""
API endpoints for agent management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....db.base import get_db
from ....db.models.agent import Agent, AgentStatus
from ....schemas.agent import AgentCreate, AgentUpdate, AgentResponse

router = APIRouter()

@router.post("/", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent"""
    db_agent = Agent(
        name=agent.name,
        type=agent.type,
        status=AgentStatus.IDLE,
        version="0.1.0",
        capabilities=agent.capabilities,
        config=agent.config,
        performance_metrics={},
        memory_usage=0.0,
        learning_state={}
    )
    db.add(db_agent)
    try:
        db.commit()
        db.refresh(db_agent)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_agent

@router.get("/", response_model=List[AgentResponse])
def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all agents"""
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent properties"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent, field, value)
    
    try:
        db.commit()
        db.refresh(db_agent)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_agent

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        db.delete(db_agent)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/status", response_model=AgentResponse)
def update_agent_status(
    agent_id: int,
    new_status: AgentStatus,
    db: Session = Depends(get_db)
):
    """Update agent status with validation"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    if not db_agent.transition_status(new_status):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status transition from {db_agent.status} to {new_status}"
        )
    
    try:
        db.commit()
        db.refresh(db_agent)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_agent
