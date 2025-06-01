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

### LLM Providers Configuration

This assistant integrates with multiple AI providers through LangChain. To set up the required credentials:

1. Create a `.env` file in the project root with the following variables (add only the providers you want to use):

```
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Google Vertex AI
GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id_here

# Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

At least one provider must be configured for the LLM client to initialize successfully.

## Usage Examples

### Using the LLM Client

```python
from jira_assistant.llm_client import LLMClient

# Initialize the client (loads credentials from environment variables)
llm_client = LLMClient()

# Generate text using the default provider
response = llm_client.generate("Summarize the key features of Jira")

# Generate text using a specific provider
response = llm_client.generate(
    "Explain agile development practices in Jira",
    provider="claude"  # Options: "openai", "vertex", "claude"
)

print(response)
```

## License

MIT 