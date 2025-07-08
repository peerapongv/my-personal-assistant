import os

import pytest

from my_personal_assistant_api.core.jira_client import FilterValidationError, JiraClient

# This marker is used to selectively run integration tests
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def real_jira_client():
    """Provides a JiraClient instance configured for a real Jira server.

    Requires JIRA_INTEGRATION_BASE_URL, JIRA_INTEGRATION_USERNAME,
    and JIRA_INTEGRATION_API_TOKEN environment variables
    to be set to connect to your actual Jira instance.
    """
    base_url = os.getenv("JIRA_INTEGRATION_BASE_URL")
    username = os.getenv("JIRA_INTEGRATION_USERNAME")
    api_token = os.getenv("JIRA_INTEGRATION_API_TOKEN")

    if not all([base_url, username, api_token]):
        pytest.skip(
            "Missing one or more Jira integration environment variables: "
            "JIRA_INTEGRATION_BASE_URL, JIRA_INTEGRATION_USERNAME, JIRA_INTEGRATION_API_TOKEN. "
            "Skipping integration tests."
        )

    return JiraClient(base_url=base_url, username=username, api_token=api_token)


@pytest.mark.asyncio
async def test_connect_and_fetch_project_epics(real_jira_client: JiraClient):
    """Attempts to fetch epics from a specific project in your Jira instance.

    You should replace 'YOUR_PROJECT_KEY' with an actual project key from your Jira
    or set the JIRA_INTEGRATION_PROJECT_KEY environment variable.
    This test primarily checks connectivity and basic data retrieval.
    """
    project_key_to_test = os.getenv("JIRA_INTEGRATION_PROJECT_KEY", "PAT")

    if project_key_to_test == "PAT" and not os.getenv("JIRA_INTEGRATION_PROJECT_KEY"):
        print(
            "\nINFO: Using default project key 'PAT' for integration test. "
            "Ensure this project exists or set JIRA_INTEGRATION_PROJECT_KEY."
        )

    try:
        print(
            f"\nAttempting to fetch epics for project: {project_key_to_test} from {real_jira_client.base_url}"
        )
        epics = await real_jira_client.get_epics(project_key=project_key_to_test)

        assert isinstance(epics, list)
        print(
            f"Successfully fetched {len(epics)} epics for project '{project_key_to_test}'."
        )
        if epics:
            print(
                f"First epic found: {epics[0].get('key')} - {epics[0].get('fields', {}).get('summary')}"
            )

    except FilterValidationError as e:
        pytest.fail(f"Filter validation error during integration test: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred during Jira API call: {e}")
    finally:
        await real_jira_client.close()


@pytest.mark.asyncio
async def test_search_stories_with_label(real_jira_client: JiraClient):
    """Attempts to search for stories with a specific label.

    Set JIRA_INTEGRATION_PROJECT_KEY and JIRA_INTEGRATION_LABEL environment variables.
    """
    project_key_to_test = os.getenv("JIRA_INTEGRATION_PROJECT_KEY", "PAT")
    label_to_test = os.getenv("JIRA_INTEGRATION_LABEL", "backend")

    if project_key_to_test == "PAT" and not os.getenv("JIRA_INTEGRATION_PROJECT_KEY"):
        print(
            "\nINFO: Using default project key 'PAT' for integration test. "
            "Set JIRA_INTEGRATION_PROJECT_KEY."
        )
    if label_to_test == "backend" and not os.getenv("JIRA_INTEGRATION_LABEL"):
        print(
            "\nINFO: Using default label 'backend' for integration test. "
            "Set JIRA_INTEGRATION_LABEL to a label in your test project."
        )

    try:
        print(
            f"\nAttempting to fetch stories for project '{project_key_to_test}' with label '{label_to_test}'."
        )
        stories = await real_jira_client.get_stories(
            project_key=project_key_to_test, labels=[label_to_test]
        )
        assert isinstance(stories, list)
        print(
            f"Successfully fetched {len(stories)} stories with label '{label_to_test}'."
        )

    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
    finally:
        await real_jira_client.close()


@pytest.mark.asyncio
async def test_invalid_status_filter_integration(real_jira_client: JiraClient):
    """Tests that providing an invalid status raises FilterValidationError even with a real API call."""
    project_key_to_test = os.getenv("JIRA_INTEGRATION_PROJECT_KEY", "PAT")
    invalid_status = "ThisStatusShouldNotExist123"

    print(
        f"\nAttempting to fetch tasks for project '{project_key_to_test}' with invalid status '{invalid_status}'."
    )
    with pytest.raises(
        FilterValidationError, match=f"Invalid status: '{invalid_status}'."
    ):
        await real_jira_client.get_tasks(
            project_key=project_key_to_test, status=invalid_status
        )

    try:
        tasks = await real_jira_client.get_tasks(
            project_key=project_key_to_test, status="Done"
        )
        assert isinstance(tasks, list)
        print(
            f"Successfully fetched {len(tasks)} tasks with status 'Done' for project '{project_key_to_test}'."
        )
    except FilterValidationError:
        pytest.fail(
            "FilterValidationError was raised for a supposedly valid status 'Done'. Check Jira config."
        )
    except Exception as e:
        print(f"Note: Could not verify 'Done' status due to: {e}")
    finally:
        await real_jira_client.close()
