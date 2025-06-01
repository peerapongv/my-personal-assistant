"""Main FastAPI application for My Personal Assistant API."""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from my_personal_assistant_api.core.llm_client import LLMClient, ConfigurationError
from my_personal_assistant_shared.types.llm import LLMProvider, LLMRequest, LLMResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="My Personal Assistant API",
    description="API for My Personal Assistant",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM client
try:
    llm_client = LLMClient()
except ConfigurationError as e:
    logger.error(f"Failed to initialize LLM client: {e}")
    llm_client = None


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint returning API information."""
    return {
        "name": "My Personal Assistant API",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    if llm_client is None:
        raise HTTPException(
            status_code=503, detail="LLM client not initialized properly"
        )
    return {"status": "healthy"}


@app.post("/generate", response_model=LLMResponse)
async def generate_text(request: LLMRequest) -> LLMResponse:
    """Generate text using the configured LLM providers."""
    if llm_client is None:
        raise HTTPException(
            status_code=503, detail="LLM client not initialized properly"
        )

    try:
        # Convert enum to string if provided
        provider_str = request.provider.value if request.provider else None

        # Generate response using the LLM client
        response_text = llm_client.generate(
            request.prompt, provider=provider_str, **request.parameters
        )

        # Get the provider that was actually used
        used_provider = provider_str or llm_client.default_provider

        # Create and return the response
        return LLMResponse(
            text=response_text,
            provider=LLMProvider(used_provider),
            metadata={"source": "my_personal_assistant_api"},
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
