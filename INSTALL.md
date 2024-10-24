# Installation Guide

This project uses Poetry for dependency management and packaging. Follow these steps to set up and run the project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installing Poetry

### Windows
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Linux/MacOS
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Add Poetry to your PATH

#### Windows
Add `%APPDATA%\Python\Scripts` to your PATH environment variable

#### Linux/MacOS
Poetry is typically installed to `$HOME/.local/bin`

## Installing the Project

1. Clone the repository:
```bash
git clone https://github.com/username/agentic-llm
cd agentic-llm
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Development Commands

- Run tests:
```bash
poetry run pytest
```

- Format code:
```bash
poetry run black .
```

## Troubleshooting

### Common Issues

1. If Poetry is not found after installation:
   - Ensure Poetry is in your PATH
   - Try restarting your terminal

2. If installation fails with dependency conflicts:
   - Update Poetry: `poetry self update`
   - Clear Poetry cache: `poetry cache clear . --all`

3. For permission errors on Linux/MacOS:
   - Use: `sudo chown -R $USER ~/.local/`

### Getting Help

If you encounter any issues:
1. Check the [Poetry documentation](https://python-poetry.org/docs/)
2. Open an issue in our repository
3. Contact the development team

## Updating Dependencies

To update project dependencies:
```bash
poetry update
```

To add new dependencies:
```bash
poetry add package-name
```

To add development dependencies:
```bash
poetry add --group dev package-name
```
