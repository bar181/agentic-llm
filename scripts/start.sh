#!/bin/bash
set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set environment variables
export PYTHONPATH=src:${PYTHONPATH}

# Check if database exists, create if not
if [ ! -f "agentic_llm.db" ]; then
    echo "Initializing database..."
    python -c "from agentic_llm.db.base import Base, engine; Base.metadata.create_all(bind=engine)"
fi

# Start the application
echo "Starting Agentic LLM..."
python src/main.py
