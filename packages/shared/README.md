# My Personal Assistant Shared

Shared code, utilities, and type definitions for the My Personal Assistant monorepo.

## Purpose

This package contains code that is shared between different packages in the My Personal Assistant monorepo:

- Common data models and type definitions
- Shared utilities and helper functions
- Constants and configuration shared across packages

## Development

### Setup

```bash
# From the monorepo root
cd packages/shared

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e ".[dev]"
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=my_personal_assistant_shared
```

## Usage

This package is intended to be used as a dependency by other packages in the monorepo. It provides shared functionality to ensure consistency across the codebase.
