"""Jira client module for interacting with Jira DC v9.4.9 REST API."""
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field, HttpUrl, validator
from tenacity import retry, stop_after_attempt, wait_exponential

class JiraConfig(BaseModel):
    """Configuration for Jira client."""
    base_url: HttpUrl = Field(..., description="Base URL of Jira instance")
    username: str = Field(..., description="Jira username")
    api_token: str = Field(..., description="Jira API token")
    timeout: int = Field(default=30, description="Request timeout in seconds")

    @validator("base_url")
    def ensure_trailing_slash(cls, v: HttpUrl) -> HttpUrl:
        """Ensure base URL ends with a trailing slash."""
        if not str(v).endswith("/"):
            return HttpUrl(str(v) + "/")
        return v

class FilterValidationError(Exception):
    """Raised when filter validation fails."""
    pass

class JiraClient:
    """Client for interacting with Jira REST API."""

    def __init__(self, config: JiraConfig):
        """Initialize Jira client with configuration."""
        self.config = config
        self._client = httpx.AsyncClient(
            base_url=str(config.base_url),
            auth=(config.username, config.api_token),
            timeout=config.timeout,
            headers={"Accept": "application/json"},
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.aclose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to Jira API with retry logic."""
        url = urljoin(str(self.config.base_url), endpoint)
        response = await self._client.request(method, url, params=params)
        response.raise_for_status()
        return response.json()

    def _build_jql_query(
        self,
        issue_type: str,
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """Build JQL query string from filter parameters."""
        conditions = [f'issuetype = "{issue_type}"']
        
        if labels:
            conditions.append(f'labels in ({", ".join(f"\"{label}\"" for label in labels)})')
        if assignee:
            conditions.append(f'assignee = "{assignee}"')
        if status:
            conditions.append(f'status = "{status}"')
            
        return " AND ".join(conditions)

    async def get_epics(
        self,
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get epics with optional filters."""
        jql = self._build_jql_query("Epic", labels, assignee, status)
        response = await self._make_request(
            "GET",
            "rest/api/2/search",
            params={"jql": jql, "maxResults": 100},
        )
        return response.get("issues", [])

    async def get_stories(
        self,
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get stories with optional filters."""
        jql = self._build_jql_query("Story", labels, assignee, status)
        response = await self._make_request(
            "GET",
            "rest/api/2/search",
            params={"jql": jql, "maxResults": 100},
        )
        return response.get("issues", [])

    async def get_tasks(
        self,
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get tasks with optional filters."""
        jql = self._build_jql_query("Task", labels, assignee, status)
        response = await self._make_request(
            "GET",
            "rest/api/2/search",
            params={"jql": jql, "maxResults": 100},
        )
        return response.get("issues", []) 