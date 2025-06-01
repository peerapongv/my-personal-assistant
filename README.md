# My Personal Assistant Monorepo

AI-driven Python Personal Assistant for Jira with a modern UI.

## Project Structure

This project is organized as a monorepo with the following structure:

```
my-personal-assistant/
├── packages/                   # All packages live here
│   ├── api/                    # Backend API service
│   │   ├── src/                # API source code
│   │   ├── tests/              # API tests
│   │   ├── pyproject.toml      # API package config
│   │   └── README.md           # API documentation
│   │
│   ├── ui/                     # Frontend UI application
│   │   ├── public/             # Static assets
│   │   ├── src/                # UI source code
│   │   ├── package.json        # UI dependencies
│   │   └── README.md           # UI documentation
│   │
│   └── shared/                 # Shared code/types
│       ├── src/                # Shared source code
│       ├── tests/              # Shared tests
│       ├── pyproject.toml      # Shared package config
│       └── README.md           # Shared package docs
│
├── scripts/                    # Monorepo management scripts
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Main project documentation
└── pyproject.toml              # Root project configuration
```

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- Git

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd my-personal-assistant
```

### 2. Set Up Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install shared package
cd packages/shared
pip install -e ".[dev]"

# Install API package
cd ../api
pip install -e ".[dev]"
```

### 3. Set Up Frontend

```bash
# Install UI dependencies
cd ../ui
npm install
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Google Vertex AI
GOOGLE_CLOUD_PROJECT=your_google_cloud_project_id_here

# Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Development

### Running the API Server

```bash
cd packages/api
uvicorn my_personal_assistant_api.main:app --reload
```

The API will be available at http://localhost:8000

### Running the UI Development Server

```bash
cd packages/ui
npm start
```

The UI will be available at http://localhost:3000

### Handling UI Dependencies

The UI package uses React with Material UI. Due to the nature of JavaScript dependencies, you might see warnings or vulnerabilities when installing packages. These are common in React projects and can be handled in several ways:

```bash
# Install with legacy peer dependencies flag (recommended for development)
npm install --legacy-peer-deps

# Fix non-breaking vulnerabilities
npm audit fix

# If you need to update dependencies to resolve security issues
npm update
```

For production deployment, you may want to address these vulnerabilities, but for development purposes, the current setup should work fine.

## Root pyproject.toml Purpose

The root `pyproject.toml` file serves several important functions in the monorepo:

1. **Project Identification**: Defines the monorepo as a whole project
2. **Development Tools Configuration**: Contains shared settings for tools like ruff and mypy
3. **Workspace Recognition**: Helps IDEs and tools recognize the project structure
4. **Cross-Package Scripts**: Can define scripts that operate across multiple packages

Each package also has its own `pyproject.toml` file that defines package-specific dependencies and configurations.

## VSCode Setup for Monorepo

For the best development experience in VSCode with this monorepo, create a workspace configuration:

1. Create a `.vscode/settings.json` file in the project root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/packages/api/src",
    "${workspaceFolder}/packages/shared/src"
  ],
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.mypyPath": "${workspaceFolder}/venv/bin/mypy",
  "python.linting.lintOnSave": true,
  "python.formatting.provider": "none",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true,
    "**/node_modules": true
  }
}
```

2. Create a `.vscode/extensions.json` file to recommend useful extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "charliermarsh.ruff",
    "ms-python.vscode-pylance",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint"
  ]
}
```

## Testing

### Backend Tests

```bash
# Run API tests
cd packages/api
pytest

# Run shared package tests
cd ../shared
pytest
```

### Frontend Tests

```bash
# Run UI tests
cd packages/ui
npm test
```

## Quick Setup with setup-dev.sh

The monorepo includes a setup script that automates the development environment setup process:

```bash
# Make the script executable
chmod +x scripts/setup-dev.sh

# Run the setup script
./scripts/setup-dev.sh
```

This script will:
1. Create a virtual environment if it doesn't exist
2. Activate the virtual environment
3. Install the shared package in development mode
4. Install the API package in development mode
5. Install UI dependencies with npm

After running the script, you can start the API and UI servers as described in the Development section.

## Monorepo Structure Benefits

This monorepo structure provides several advantages:

1. **Separation of Concerns**: Each package has a clear responsibility
   - API: Backend services and LLM integration
   - UI: Frontend user interface
   - Shared: Common types and utilities

2. **Independent Development**: Teams can work on different packages simultaneously

3. **Consistent Tooling**: Shared configuration for linting, formatting, and testing

4. **Simplified Dependencies**: Each package manages its own dependencies

5. **Code Sharing**: The shared package enables code reuse without duplication

## Troubleshooting

### Common UI Setup Issues

1. **Node.js Version Conflicts**
   - **Symptom**: OpenSSL errors when starting the UI
   - **Solution**: The package.json scripts use the `--openssl-legacy-provider` flag to handle this

2. **Dependency Conflicts**
   - **Symptom**: Error messages about peer dependencies or version conflicts
   - **Solution**: Use `npm install --legacy-peer-deps` or `npm install --force`

3. **Port Already in Use**
   - **Symptom**: "Something is already running on port 3000"
   - **Solution**: Kill the existing process or use a different port: `PORT=3001 npm start`

4. **Security Vulnerabilities**
   - **Symptom**: npm audit shows vulnerabilities
   - **Solution**: For development, these can often be ignored. For production, run `npm audit fix`

### Common API Setup Issues

1. **Missing Dependencies**
   - **Symptom**: ImportError when running the API
   - **Solution**: Ensure you've installed the package in development mode: `pip install -e ".[dev]"`

2. **Environment Variables**
   - **Symptom**: ConfigurationError when initializing LLM client
   - **Solution**: Check that your .env file contains at least one LLM provider's credentials

## License

MIT
