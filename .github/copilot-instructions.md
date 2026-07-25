# Project Instructions for GitHub Copilot

## Project Overview
This is a Python project demonstrating best practices for Python development with proper structure, virtual environment management, and testing.

## Project Structure
- `src/` - Main source code directory
- `tests/` - Unit tests directory
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation

## Getting Started

### 1. Virtual Environment Setup
Create and activate a Python virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Project
```bash
python src/main.py
```

## Development Workflow
- Write code in the `src/` directory
- Create tests in the `tests/` directory
- Follow PEP 8 style guidelines
- Update `requirements.txt` when adding new dependencies

## Code Style
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and maintainable
- Add type hints where appropriate
