"""Tests for the example module."""

from jira_assistant.example import hello_world


def test_hello_world() -> None:
    """Test the hello_world function."""
    assert hello_world() == "Hello, Jira Assistant!"
