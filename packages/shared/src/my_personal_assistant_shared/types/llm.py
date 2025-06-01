"""LLM-related type definitions."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    VERTEX = "vertex"
    CLAUDE = "claude"


class LLMRequest(BaseModel):
    """Request model for LLM generation."""

    prompt: str = Field(..., description="The prompt to send to the LLM")
    provider: Optional[LLMProvider] = Field(
        None, description="The LLM provider to use (defaults to configured default)"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Additional parameters to pass to the LLM"
    )


class LLMResponse(BaseModel):
    """Response model for LLM generation."""

    text: str = Field(..., description="The generated text response")
    provider: LLMProvider = Field(..., description="The LLM provider that was used")
    tokens: Optional[Dict[str, int]] = Field(
        None, description="Token usage information if available"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the response"
    )
