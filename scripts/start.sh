#!/bin/bash

# Activate virtual environment if using one
# source .venv/bin/activate

# Set environment variables
export PYTHONPATH=src:${PYTHONPATH}

# Start the application
python src/main.py
