"""Jira-related type definitions."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class JiraIssueStatus(str, Enum):
    """Common Jira issue statuses."""

    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"
    BLOCKED = "Blocked"


class JiraIssuePriority(str, Enum):
    """Jira issue priorities."""

    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"


class JiraIssueType(str, Enum):
    """Common Jira issue types."""

    EPIC = "Epic"
    STORY = "Story"
    TASK = "Task"
    BUG = "Bug"
    SUBTASK = "Sub-task"


class JiraUser(BaseModel):
    """Jira user information."""

    id: str = Field(..., description="User ID")
    display_name: str = Field(..., description="User display name")
    email: Optional[str] = Field(None, description="User email address")
    avatar_url: Optional[str] = Field(None, description="URL to user avatar")


class JiraIssueReference(BaseModel):
    """Basic reference to a Jira issue."""

    key: str = Field(..., description="Issue key (e.g., 'PROJ-123')")
    id: str = Field(..., description="Issue ID")
    summary: str = Field(..., description="Issue summary")


class JiraIssue(JiraIssueReference):
    """Detailed Jira issue information."""

    description: Optional[str] = Field(None, description="Issue description")
    status: JiraIssueStatus = Field(..., description="Current issue status")
    issue_type: JiraIssueType = Field(..., description="Issue type")
    priority: Optional[JiraIssuePriority] = Field(None, description="Issue priority")
    assignee: Optional[JiraUser] = Field(None, description="Assigned user")
    reporter: Optional[JiraUser] = Field(None, description="Issue reporter")
    created: datetime = Field(..., description="Creation timestamp")
    updated: datetime = Field(..., description="Last update timestamp")
    parent: Optional[JiraIssueReference] = Field(
        None, description="Parent issue if any"
    )
    labels: List[str] = Field(default_factory=list, description="Issue labels")
    components: List[str] = Field(default_factory=list, description="Issue components")
    fields: Dict[str, Any] = Field(
        default_factory=dict, description="Additional custom fields"
    )
