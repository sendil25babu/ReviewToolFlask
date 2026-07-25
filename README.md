# Python Project

A well-structured Python project with best practices for development.

## Features
- Clean project structure with separated source and test directories
- Virtual environment setup for dependency management
- Ready-to-use project template

## Requirements
- Python 3.8 or higher

## Installation

1. **Clone or navigate to the project:**
   ```bash
   cd ReviewToolCon
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```bash
python src/main.py
```

## Project Structure
```
ReviewToolCon/
├── src/
│   └── main.py          # Main entry point
├── tests/               # Test directory
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
└── .github/
    └── copilot-instructions.md  # Copilot instructions
```

## Contributing
When adding new features:
1. Create code in the `src/` directory
2. Write tests in the `tests/` directory
3. Update `requirements.txt` if adding dependencies
4. Follow PEP 8 style guidelines

## License
This project is open source.
