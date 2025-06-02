"""Jira API router."""
import os
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from my_personal_assistant_api.clients.jira_client import JiraClient, JiraConfig

router = APIRouter(prefix="/jira", tags=["jira"])

class JiraIssue(BaseModel):
    """Jira issue model."""
    id: str
    key: str
    summary: str
    issue_type: str
    status: str
    assignee: Optional[str]
    labels: List[str]

def get_jira_client() -> JiraClient:
    """Get Jira client instance."""
    config = JiraConfig(
        base_url=HttpUrl(os.getenv("JIRA_BASE_URL", "https://your-jira-instance.com/")),
        username=os.getenv("JIRA_USERNAME", "your-username"),
        api_token=os.getenv("JIRA_API_TOKEN", "your-api-token"),
    )
    return JiraClient(config)

@router.get("/epics", response_model=List[JiraIssue])
async def get_epics(
    labels: Optional[List[str]] = None,
    assignee: Optional[str] = None,
    status: Optional[str] = None,
    client: JiraClient = Depends(get_jira_client),
):
    """Get epics with optional filters."""
    try:
        issues = await client.get_epics(labels, assignee, status)
        return [
            JiraIssue(
                id=issue["id"],
                key=issue["key"],
                summary=issue["fields"]["summary"],
                issue_type=issue["fields"]["issuetype"]["name"],
                status=issue["fields"]["status"]["name"],
                assignee=issue["fields"]["assignee"]["name"] if issue["fields"]["assignee"] else None,
                labels=issue["fields"]["labels"],
            )
            for issue in issues
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stories", response_model=List[JiraIssue])
async def get_stories(
    labels: Optional[List[str]] = None,
    assignee: Optional[str] = None,
    status: Optional[str] = None,
    client: JiraClient = Depends(get_jira_client),
):
    """Get stories with optional filters."""
    try:
        issues = await client.get_stories(labels, assignee, status)
        return [
            JiraIssue(
                id=issue["id"],
                key=issue["key"],
                summary=issue["fields"]["summary"],
                issue_type=issue["fields"]["issuetype"]["name"],
                status=issue["fields"]["status"]["name"],
                assignee=issue["fields"]["assignee"]["name"] if issue["fields"]["assignee"] else None,
                labels=issue["fields"]["labels"],
            )
            for issue in issues
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks", response_model=List[JiraIssue])
async def get_tasks(
    labels: Optional[List[str]] = None,
    assignee: Optional[str] = None,
    status: Optional[str] = None,
    client: JiraClient = Depends(get_jira_client),
):
    """Get tasks with optional filters."""
    try:
        issues = await client.get_tasks(labels, assignee, status)
        return [
            JiraIssue(
                id=issue["id"],
                key=issue["key"],
                summary=issue["fields"]["summary"],
                issue_type=issue["fields"]["issuetype"]["name"],
                status=issue["fields"]["status"]["name"],
                assignee=issue["fields"]["assignee"]["name"] if issue["fields"]["assignee"] else None,
                labels=issue["fields"]["labels"],
            )
            for issue in issues
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 