"""Test script for LLMClient."""

import logging

from my_personal_assistant_api.core.llm_client import LLMClient

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_llm_client():
    """Test the LLMClient with a simple prompt using OpenAI."""
    try:
        # Initialize the client with only OpenAI
        logger.info("Initializing LLMClient with OpenAI...")
        client = LLMClient()

        # Verify OpenAI is available
        if "openai" not in client.clients:
            raise RuntimeError(
                "OpenAI client not initialized. "
                "Please check your OPENAI_API_KEY in .env file"
            )

        # Test with a simple prompt
        prompt = "Tell me a short joke about programming"
        logger.info(f"Sending prompt: {prompt}")

        # Generate response
        response = client.generate(prompt)

        # Print results
        print("\n=== Test Results ===")
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print("==================")
        logger.info("Test completed successfully!")

    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    test_llm_client()
