import os
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

JIRA_API_VERSION = "rest/api/2"


class FilterValidationError(ValueError):
    """Custom exception for invalid filter parameters."""

    pass


class JiraClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        api_token: Optional[str] = None,
    ):
        self.base_url = base_url or os.getenv("JIRA_BASE_URL")
        self.username = username or os.getenv("JIRA_USERNAME")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN")

        if not self.base_url:
            raise ValueError(
                "Jira base URL must be provided or set as JIRA_BASE_URL "
                "environment variable."
            )
        if not self.username:
            raise ValueError(
                "Jira username must be provided or set as JIRA_USERNAME "
                "environment variable."
            )
        if not self.api_token:
            raise ValueError(
                "Jira API token must be provided or set as JIRA_API_TOKEN "
                "environment variable."
            )

        self.api_base_url = urljoin(self.base_url, f"{JIRA_API_VERSION}/")
        self._client = httpx.AsyncClient(
            auth=(self.username, self.api_token), timeout=30.0
        )

    async def _request(
        self, method: str, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Helper method to make authenticated requests to Jira API."""
        url = urljoin(self.api_base_url, endpoint)
        try:
            response = await self._client.request(method, url, params=params)
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses
            return response.json()
        except httpx.HTTPStatusError as e:
            # Log error or handle specific statuses
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            # Log error or handle network issues
            print(f"Request error occurred: {e}")
            raise

    def _build_jql_query(
        self,
        project_key: Optional[str] = None,
        issue_types: Optional[list[str]] = None,
        labels: Optional[list[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
    ) -> str:
        """Builds a JQL query string from filter parameters."""
        jql_parts = []
        if project_key:
            jql_parts.append(f"project = {project_key}")

        if issue_types:
            types_list = [f'"{it}"' for it in issue_types]
            types_str = ", ".join(types_list)  # Enclose in quotes for JQL
            jql_parts.append(f"issueType in ({types_str})")

        if labels:
            # Assuming labels are single words without spaces, or handled by Jira's JQL parsing
            labels_list = [f'"{label}"' for label in labels]
            labels_str = ", ".join(labels_list)
            jql_parts.append(f"labels in ({labels_str})")

        if assignee:
            # Assignee can be username or display name, Jira handles this.
            # For unassigned, use assignee is EMPTY or assignee is NULL
            jql_parts.append(f'assignee = "{assignee}"')  # Enclose in quotes

        if status:
            allowed_statuses = [
                "To Do",
                "In Progress",
                "Done",
                "Backlog",
                "Selected for Development",
            ]
            if status not in allowed_statuses:
                error_part1 = f"Invalid status: '{status}'. "
                error_part2 = "Allowed statuses are: "
                error_part3 = ", ".join(allowed_statuses)
                full_error_message = error_part1 + error_part2 + error_part3
                raise FilterValidationError(full_error_message)
            # Status names can have spaces, so enclose in quotes
            jql_parts.append(f'status = "{status}"')

        return " AND ".join(jql_parts)

    async def search_issues(
        self,
        jql: str,
        fields: Optional[list[str]] = None,
        start_at: int = 0,
        max_results: int = 50,
    ) -> dict[str, Any]:
        """Performs a JQL search."""
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
        }
        if fields:
            params["fields"] = ",".join(fields)
        else:
            # Default fields, can be adjusted
            params["fields"] = (
                "summary,status,assignee,labels,issuetype,priority,"
                "reporter,created,updated,duedate,parent"
            )

        return await self._request("GET", "search", params=params)

    async def get_epics(
        self,
        project_key: Optional[str] = None,
        labels: Optional[list[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """Retrieves Epics, optionally filtered."""
        jql = self._build_jql_query(
            project_key=project_key,
            issue_types=["Epic"],
            labels=labels,
            assignee=assignee,
            status=status,
        )
        # Add specific Epic fields if necessary, e.g., 'customfield_XXXXX' for Epic Name
        # For now, using default fields from search_issues
        response_data = await self.search_issues(jql, fields=fields)
        return response_data.get("issues", [])

    async def get_stories(
        self,
        project_key: Optional[str] = None,
        labels: Optional[list[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """Retrieves Stories, optionally filtered."""
        jql = self._build_jql_query(
            project_key=project_key,
            issue_types=["Story"],
            labels=labels,
            assignee=assignee,
            status=status,
        )
        response_data = await self.search_issues(jql, fields=fields)
        return response_data.get("issues", [])

    async def get_tasks(
        self,
        project_key: Optional[str] = None,
        labels: Optional[list[str]] = None,
        assignee: Optional[str] = None,
        status: Optional[str] = None,
        fields: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """Retrieves Tasks, optionally filtered."""
        # Assuming 'Task' is the standard issue type name. It might be 'Sub-task' or custom.
        jql = self._build_jql_query(
            project_key=project_key,
            issue_types=[
                "Task",
                "Sub-task",
            ],  # Or make this configurable
            labels=labels,
            assignee=assignee,
            status=status,
        )
        response_data = await self.search_issues(jql, fields=fields)
        return response_data.get("issues", [])

    async def close(self):
        """Closes the underlying HTTP client."""
        await self._client.aclose()


# Example Usage (for testing purposes, remove or guard with if __name__ == "__main__")
# import asyncio
# async def main():
#     # Ensure JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN are set in your environment
#     # Or pass them directly:
#     # JiraClient(
#     #     base_url="https://your-jira.atlassian.net",
#     #     username="email",
#     #     api_token="token"
#     # )
#     client = JiraClient()
#     try:
#         print("Fetching Epics...")
#         epics = await client.get_epics(project_key="PAT") # Replace 'PAT' with your project key
#         for epic in epics:
#             print(f"  Epic: {epic.get('key')} - {epic.get('fields', {}).get('summary')}")

#         print("\nFetching Stories with label 'backend'...")
#         stories = await client.get_stories(project_key="PAT", labels=["backend"])
#         for story in stories:
#             print(f"  Story: {story.get('key')} - {story.get('fields', {}).get('summary')}")

#         print("\nFetching Tasks assigned to 'mork'...")
#         tasks = await client.get_tasks(project_key="PAT", assignee="mork") # Replace 'mork' with a valid assignee
#         for task in tasks:
#             print(f"  Task: {task.get('key')} - {task.get('fields', {}).get('summary')}")

#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         await client.close()

# if __name__ == "__main__":
# asyncio.run(main())
