# Jira Assistant

AI-driven Python Personal Assistant for Jira.

## Prerequisites

- Python 3.9 or higher
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd jira-assistant
```

### 2. Set Up Virtual Environment

#### On macOS/Linux:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install the project in development mode with all dependencies
pip install -e ".[dev]"
```

### 4. Verify Installation

```bash
# Test the installation
python -c "from jira_assistant.example import hello_world; print(hello_world())"
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=jira_assistant
```

### Code Quality

```bash
# Run linting
ruff .

# Run type checking
mypy .
```

### Project Structure

```
.
├── .github/
│   └── workflows/        # GitHub Actions CI configuration
├── src/
│   └── jira_assistant/  # Main package code
├── tests/               # Test files
├── README.md           # This file
└── pyproject.toml      # Project configuration and dependencies
```

## Configuration

The project uses `pyproject.toml` for configuration, which includes:
- Project metadata
- Dependencies
- Development tools configuration (Ruff, mypy, pytest)

## License

MIT 