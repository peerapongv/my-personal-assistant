"""Tests for Jira client module."""
import pytest
import httpx
from httpx import Response
from pydantic import HttpUrl

from my_personal_assistant_api.clients.jira_client import (
    JiraClient,
    JiraConfig,
    FilterValidationError,
)

@pytest.fixture
def jira_config():
    """Create a test Jira configuration."""
    return JiraConfig(
        base_url=HttpUrl("https://test-jira.example.com/"),
        username="test-user",
        api_token="test-token",
    )

@pytest.fixture
def mock_issues_response():
    """Create a mock Jira issues response."""
    return {
        "issues": [
            {
                "id": "10001",
                "key": "TEST-1",
                "fields": {
                    "summary": "Test Issue",
                    "issuetype": {"name": "Task"},
                    "status": {"name": "To Do"},
                    "assignee": {"name": "test-user"},
                    "labels": ["test", "backend"],
                },
            }
        ]
    }

@pytest.mark.asyncio
async def test_get_tasks_with_filters(jira_config, mock_issues_response, httpx_mock):
    """Test getting tasks with filters."""
    httpx_mock.add_response(
        method="GET",
        url="https://test-jira.example.com/rest/api/2/search",
        json=mock_issues_response,
        match_query_params={
            "jql": 'issuetype = "Task" AND labels in ("backend") AND assignee = "test-user" AND status = "To Do"',
            "maxResults": "100",
        },
    )

    async with JiraClient(jira_config) as client:
        tasks = await client.get_tasks(
            labels=["backend"],
            assignee="test-user",
            status="To Do",
        )

    assert len(tasks) == 1
    assert tasks[0]["key"] == "TEST-1"
    assert tasks[0]["fields"]["summary"] == "Test Issue"

@pytest.mark.asyncio
async def test_get_stories(jira_config, mock_issues_response, httpx_mock):
    """Test getting stories."""
    httpx_mock.add_response(
        method="GET",
        url="https://test-jira.example.com/rest/api/2/search",
        json=mock_issues_response,
        match_query_params={
            "jql": 'issuetype = "Story"',
            "maxResults": "100",
        },
    )

    async with JiraClient(jira_config) as client:
        stories = await client.get_stories()

    assert len(stories) == 1
    assert stories[0]["key"] == "TEST-1"

@pytest.mark.asyncio
async def test_get_epics(jira_config, mock_issues_response, httpx_mock):
    """Test getting epics."""
    httpx_mock.add_response(
        method="GET",
        url="https://test-jira.example.com/rest/api/2/search",
        json=mock_issues_response,
        match_query_params={
            "jql": 'issuetype = "Epic"',
            "maxResults": "100",
        },
    )

    async with JiraClient(jira_config) as client:
        epics = await client.get_epics()

    assert len(epics) == 1
    assert epics[0]["key"] == "TEST-1"

@pytest.mark.asyncio
async def test_http_error_handling(jira_config, httpx_mock):
    """Test handling of HTTP errors."""
    httpx_mock.add_response(
        method="GET",
        url="https://test-jira.example.com/rest/api/2/search",
        status_code=401,
    )

    async with JiraClient(jira_config) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_tasks()

def test_jira_config_validation():
    """Test Jira configuration validation."""
    # Test valid configuration
    config = JiraConfig(
        base_url=HttpUrl("https://test-jira.example.com"),
        username="test-user",
        api_token="test-token",
    )
    assert str(config.base_url).endswith("/")

    # Test invalid URL
    with pytest.raises(ValueError):
        JiraConfig(
            base_url=HttpUrl("invalid-url"),
            username="test-user",
            api_token="test-token",
        ) 