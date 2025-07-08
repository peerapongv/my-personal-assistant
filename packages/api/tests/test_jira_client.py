from unittest.mock import AsyncMock, patch

import httpx
import pytest

from my_personal_assistant_api.core.jira_client import FilterValidationError, JiraClient


# Fixtures
@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("JIRA_BASE_URL", "https://test.jira.com")
    monkeypatch.setenv("JIRA_USERNAME", "testuser")
    monkeypatch.setenv("JIRA_API_TOKEN", "testtoken")


@pytest.fixture
def client(mock_env_vars):
    return JiraClient()


# Tests for JiraClient Instantiation


def test_jira_client_instantiation_success(mock_env_vars):
    """Test successful instantiation with environment variables."""
    client = JiraClient()
    assert client.base_url == "https://test.jira.com"
    assert client.username == "testuser"
    assert client.api_base_url == "https://test.jira.com/rest/api/2/"


def test_jira_client_instantiation_direct_params():
    """Test successful instantiation with direct parameters."""
    client = JiraClient(
        base_url="https://direct.jira.com",
        username="directuser",
        api_token="directtoken",
    )
    assert client.base_url == "https://direct.jira.com"
    assert client.username == "directuser"


def test_jira_client_instantiation_missing_base_url(mock_env_vars, monkeypatch):
    monkeypatch.delenv("JIRA_BASE_URL")
    with pytest.raises(ValueError, match="Jira base URL must be provided"):
        JiraClient()


def test_jira_client_instantiation_missing_username(mock_env_vars, monkeypatch):
    monkeypatch.delenv("JIRA_USERNAME")
    with pytest.raises(ValueError, match="Jira username must be provided"):
        JiraClient()


def test_jira_client_instantiation_missing_api_token(mock_env_vars, monkeypatch):
    monkeypatch.delenv("JIRA_API_TOKEN")
    with pytest.raises(ValueError, match="Jira API token must be provided"):
        JiraClient()


# Tests for _build_jql_query


@pytest.mark.parametrize(
    "filters, expected_jql",
    [
        ({}, ""),
        ({"project_key": "PROJ"}, "project = PROJ"),
        ({"issue_types": ["Bug"]}, 'issueType in ("Bug")'),
        ({"labels": ["backend"]}, 'labels in ("backend")'),
        ({"assignee": "mork"}, 'assignee = "mork"'),
        ({"status": "In Progress"}, 'status = "In Progress"'),
        (
            {
                "project_key": "PROJ",
                "labels": ["frontend", "urgent"],
                "status": "To Do",
            },
            'project = PROJ AND labels in ("frontend", "urgent") AND status = "To Do"',
        ),
        (
            {"issue_types": ["Story", "Task"], "assignee": "peerapong"},
            'issueType in ("Story", "Task") AND assignee = "peerapong"',
        ),
    ],
)
def test_build_jql_query(client, filters, expected_jql):
    jql = client._build_jql_query(**filters)
    assert jql == expected_jql


def test_build_jql_query_invalid_status(client):
    with pytest.raises(
        FilterValidationError, match="Invalid status: 'Invalid Status'."
    ):
        client._build_jql_query(status="Invalid Status")


def test_build_jql_query_valid_status(client):
    jql = client._build_jql_query(status="Done")
    assert 'status = "Done"' in jql


# Tests for search_issues (mocking HTTP calls)
@pytest.mark.asyncio
async def test_search_issues_success(client, mocker):
    mock_response_data = {"issues": [{"key": "PROJ-123"}], "total": 1}

    # Mock the internal _request method
    mock_request = AsyncMock(return_value=mock_response_data)
    mocker.patch.object(client, "_request", new=mock_request)

    jql = "project = PROJ"
    response = await client.search_issues(jql)

    mock_request.assert_called_once_with(
        "GET",
        "search",
        params={
            "jql": jql,
            "startAt": 0,
            "maxResults": 50,
            "fields": "summary,status,assignee,labels,issuetype,priority,reporter,created,updated,duedate,parent",
        },
    )
    assert response == mock_response_data
    await client.close()  # Close client to avoid warnings


@pytest.mark.asyncio
async def test_search_issues_with_fields(client, mocker):
    mock_response_data = {"issues": [], "total": 0}
    mock_request = AsyncMock(return_value=mock_response_data)
    mocker.patch.object(client, "_request", new=mock_request)

    jql = "project = PROJ"
    fields = ["summary", "status"]
    await client.search_issues(jql, fields=fields)

    mock_request.assert_called_once_with(
        "GET",
        "search",
        params={"jql": jql, "startAt": 0, "maxResults": 50, "fields": "summary,status"},
    )
    await client.close()


@pytest.mark.asyncio
async def test_search_issues_http_error(client, mocker):
    # Mock _request to raise an HTTPStatusError
    mock_request = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error",
            request=AsyncMock(),
            response=AsyncMock(status_code=500, text="Server Error"),
        )
    )
    mocker.patch.object(client, "_request", new=mock_request)

    with pytest.raises(httpx.HTTPStatusError):
        await client.search_issues("project = PROJ")
    await client.close()


# Placeholder tests for get_epics, get_stories, get_tasks
# These will be similar to test_search_issues,
# verifying that the correct JQL is built and search_issues is called.


@pytest.mark.asyncio
async def test_get_epics_calls_search_issues_correctly(client, mocker):
    mock_search_issues = AsyncMock(return_value={"issues": []})
    mocker.patch.object(client, "search_issues", new=mock_search_issues)

    await client.get_epics(project_key="TEST", labels=["epic-label"], status="To Do")

    expected_jql = 'project = TEST AND issueType in ("Epic") AND labels in ("epic-label") AND status = "To Do"'
    mock_search_issues.assert_called_once_with(expected_jql, fields=None)
    await client.close()


@pytest.mark.asyncio
async def test_get_stories_calls_search_issues_correctly(client, mocker):
    mock_search_issues = AsyncMock(return_value={"issues": []})
    mocker.patch.object(client, "search_issues", new=mock_search_issues)

    await client.get_stories(project_key="TEST", assignee="user1")

    expected_jql = 'project = TEST AND issueType in ("Story") AND assignee = "user1"'
    mock_search_issues.assert_called_once_with(expected_jql, fields=None)
    await client.close()


@pytest.mark.asyncio
async def test_get_tasks_calls_search_issues_correctly(client, mocker):
    mock_search_issues = AsyncMock(return_value={"issues": []})
    mocker.patch.object(client, "search_issues", new=mock_search_issues)

    await client.get_tasks(project_key="TEST", status="In Progress")

    expected_jql = 'project = TEST AND issueType in ("Task", "Sub-task") AND status = "In Progress"'
    mock_search_issues.assert_called_once_with(expected_jql, fields=None)
    await client.close()


# Test closing the client
@pytest.mark.asyncio
async def test_client_close(client):
    # Ensure the close method can be called without error
    # and that the underlying httpx client's aclose is called.
    with patch.object(client._client, "aclose", new_callable=AsyncMock) as mock_aclose:
        await client.close()
        mock_aclose.assert_called_once()
