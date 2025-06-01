# My Personal Assistant API

Backend API service for the AI-driven My Personal Assistant.

## Features

- REST API for interacting with the My Personal Assistant
- Integration with multiple LLM providers (OpenAI, Vertex AI, Claude)
- Secure authentication and authorization
- Jira integration endpoints

## Development

### Setup

```bash
# From the monorepo root
cd packages/api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e ".[dev]"
```

### Running the API Server

```bash
# Start the development server
uvicorn my_personal_assistant_api.main:app --reload
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=my_personal_assistant_api
```

## API Documentation

When the server is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
