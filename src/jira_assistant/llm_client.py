"""LangChain client wrapper for multiple LLM providers.

This module provides a unified interface to interact with various LLM providers
(OpenAI, Vertex AI, Claude) through LangChain.

Example usage:
    from jira_assistant.llm_client import LLMClient

    # Initialize the client
    llm_client = LLMClient()

    # Generate text using the default provider
    response = llm_client.generate("Tell me about Jira")

    # Generate text using a specific provider
    response = llm_client.generate(
        "What are the best practices for Jira workflow?",
        provider="claude"
    )
"""

import logging
import os
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate
from langchain_community.llms import VertexAI
from langchain_community.llms.anthropic import Anthropic
from langchain_openai import ChatOpenAI

# Configure logging
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when there is an issue with configuration or credentials."""

    pass


class LLMClient:
    """A wrapper around LangChain's LLM clients to provide a unified interface.

    This class initializes and manages connections to multiple LLM providers,
    abstracting away the details of credential management and provider-specific
    configuration.
    """

    SUPPORTED_PROVIDERS = ("openai", "vertex", "claude")

    def __init__(self) -> None:
        """Initialize the LLM client wrapper.

        Loads credentials from environment variables and initializes
        connections to supported LLM providers.

        Raises:
            ConfigurationError: If required credentials are missing.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()

        # Initialize clients dictionary
        self.clients: dict[str, BaseLLM] = {}

        # Initialize each provider if credentials are available
        self._initialize_openai()
        self._initialize_vertex()
        self._initialize_claude()

        # Check if at least one provider is configured
        if not self.clients:
            raise ConfigurationError(
                "No LLM providers configured. Please set up credentials for "
                "at least one of the supported providers: "
                f"{', '.join(self.SUPPORTED_PROVIDERS)}"
            )

        # Set the default provider to the first available one
        self.default_provider = next(iter(self.clients.keys()))
        logger.info(f"Default provider set to: {self.default_provider}")

    def _initialize_openai(self) -> None:
        """Initialize the OpenAI client if credentials are available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.clients["openai"] = ChatOpenAI(
                    openai_api_key=api_key,
                    temperature=0.7,
                    model_name="gpt-4o",  # Default model - can be overridden
                )
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("OpenAI API key not found, skipping initialization")

    def _initialize_vertex(self) -> None:
        """Initialize the Vertex AI client if credentials are available."""
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id:
            try:
                self.clients["vertex"] = VertexAI(
                    project=project_id,
                    temperature=0.7,
                    model_name="text-bison@001",  # Default model
                )
                logger.info("Vertex AI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI client: {e}")
        else:
            logger.warning(
                "Google Cloud project ID not found, skipping Vertex AI initialization"
            )

    def _initialize_claude(self) -> None:
        """Initialize the Claude client if credentials are available."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            try:
                self.clients["claude"] = Anthropic(
                    anthropic_api_key=api_key,
                    temperature=0.7,
                    model="claude-3-sonnet-20240229",  # Correct parameter name for Anthropic
                )
                logger.info("Claude client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Claude client: {e}")
        else:
            logger.warning(
                "Anthropic API key not found, skipping Claude initialization"
            )

    def generate(
        self,
        prompt: str,
        provider: Optional[Literal["openai", "vertex", "claude"]] = None,
        **kwargs: Any,
    ) -> str:
        """Generate a response from the specified LLM provider.

        Args:
            prompt: The text prompt to send to the LLM.
            provider: The LLM provider to use. If None, uses the default provider.
            **kwargs: Additional arguments to pass to the LLM.

        Returns:
            The generated text response.

        Raises:
            ValueError: If the specified provider is not supported or not configured.
            RuntimeError: If the LLM generation fails.
        """
        # Determine which provider to use
        selected_provider = provider or self.default_provider

        # Check if the selected provider is supported
        if selected_provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {selected_provider}. "
                f"Supported providers are: {', '.join(self.SUPPORTED_PROVIDERS)}"
            )

        # Check if the selected provider is configured
        if selected_provider not in self.clients:
            raise ValueError(
                f"Provider {selected_provider} is not configured. "
                f"Configured providers are: {', '.join(self.clients.keys())}"
            )

        # Log the provider being used
        logger.info(f"Generating response using provider: {selected_provider}")

        try:
            # Get the LLM client for the selected provider
            llm = self.clients[selected_provider]

            # Create a simple prompt template and chain it with the LLM
            prompt_template = PromptTemplate.from_template("{prompt}")
            # Create a chain using the pipe operator
            chain = prompt_template | llm
            # Invoke the chain with the prompt and any additional arguments
            response = chain.invoke({"prompt": prompt, **kwargs})
            return response.strip() if isinstance(response, str) else str(response)
        except Exception as e:
            logger.error(f"Error generating response with {selected_provider}: {e}")
            raise RuntimeError(f"Failed to generate response: {str(e)}")
