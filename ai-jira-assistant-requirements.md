# AI-Driven Python Personal Assistant for Jira — Requirements Summary

## Project Definition
- **Name:** AI-driven Python Personal Assistant for Jira  
- **Key Capabilities:**  
  1. LangChain-based multi-LLM client (OpenAI, Vertex AI, Claude)  
  2. Jira DC v9.4.9 integration via REST API  
  3. Intelligent backlog analysis & hierarchical reporting  
  4. Plain-text requirements → automated Jira Epics/Stories/Sub-tasks  
  5. Automated creation of Jira tickets  
  6. (Optional) Auto-updating Markdown summary of Jira items  
  7. Monorepo structure with Backend API, Frontend UI, and Shared packages  
  8. Chatbot integration layer and IDE-based AI coding assistant via MCP server, both using a shared Jira wrapper  

---

## Epic 1: System Integration Foundation  
**Goal:** Establish robust integration with LLM providers and Jira to provide the foundation for AI-driven assistant capabilities.

### Story 1.0: Initialize Project Skeleton  
- **Summary:**  
  As a developer, I want to initialize the project skeleton, so that the codebase has a standardized structure, linting, and CI/CD toolchain in place from day one.  
- **Acceptance Criteria:**  
  - Standard Python layout (`src/`, `tests/`, `pyproject.toml`) with Ruff configured and zero violations.  
  - GitHub Actions workflow (`ci.yml`) runs lint, type-check, and tests on every push.  

#### Sub-tasks  
1. **Create Project Scaffold**  
   - **Description:**  
     Generate `src/`, `tests/`, and minimal module files; add `pyproject.toml` with metadata and Ruff settings.  
   - **Definition of Done:**  
     - Directory structure exists and imports work without errors.  
     - `ruff .` completes with zero errors.  

2. **Configure CI/CD Pipeline**  
   - **Description:**  
     Create GitHub Actions workflow to run Ruff, mypy, and pytest; include dependency caching.  
   - **Definition of Done:**  
     - `.github/workflows/ci.yml` present, running all checks successfully.  
     - README badges reflect passing status.  

---

### Story 1.1: Configure Multi-LLM Client  
- **Summary:**  
  As a developer, I want to configure the LangChain client to interface with multiple LLM providers, so that the system can generate responses from any supported model.  
- **Acceptance Criteria:**  
  - LangChain wrapper initializes OpenAI, Vertex AI, Claude clients.  
  - Credentials loaded securely; provider switch logic tested.  

#### Sub-tasks  
1. **Create LangChain Client Wrapper**  
   - **Description:**  
     Implement an `LLMClient` class exposing a unified `generate()` method, instantiating provider-specific clients under the hood. Document usage examples.  
   - **Definition of Done:**  
     - `LLMClient` exists with `__init__` and `generate()` methods.  
     - Unit tests mock each provider and verify selection logic.  

2. **Configure Credential Management**  
   - **Description:**  
     Load API keys from environment variables or `.env` via `python-dotenv`. Validate presence at startup and raise clear errors if missing.  
   - **Definition of Done:**  
     - Missing credentials trigger `ConfigurationError`.  
     - README includes setup instructions; tests cover valid/missing scenarios.  

3. **Implement Provider-Switching Logic**  
   - **Description:**  
     Add logic to select the LLM provider based on a `provider` parameter, with fallback to default. Log provider choice per request.  
   - **Definition of Done:**  
     - `generate(provider="vertex")` calls Vertex AI client.  
     - Unsupported provider raises `ValueError`; tests validate behavior.  

---

### Story 1.2: Integrate Jira Data Retrieval  
- **Summary:**  
  As a developer, I want to integrate with Jira’s REST API to fetch Epics, Stories, and Tasks (with filters), so that the assistant can access up-to-date backlog data.  
- **Acceptance Criteria:**  
  - Client methods `get_epics()`, `get_stories()`, `get_tasks()` support filters (`labels`, `assignee`, `status`).  
  - Pagination handled seamlessly; JSON matches internal schema.  

#### Sub-tasks  
1. **Develop Jira API Client Module**  
   - **Description:**  
     Build `jira_client.py` using `httpx.AsyncClient` for authentication and base URL. Stub basic GET endpoints.  
   - **Definition of Done:**  
     - Module authenticates and retrieves raw JSON from a test instance.  
     - Tests stub HTTP responses and verify parsing.  

2. **Implement Fetch Methods with Filters**  
   - **Description:**  
     Extend client to accept filter params, translate to JQL, and combine multiple filters correctly, with validation and logging.  
   - **Definition of Done:**  
     - `get_tasks(labels=["backend"], assignee="mork")` yields correct issues.  
     - Invalid filters raise `FilterValidationError`; tests cover scenarios.  

3. **Handle Jira API Pagination**  
   - **Description:**  
     Loop through paginated responses (`startAt`, `maxResults`), aggregate results, and log progress.  
   - **Definition of Done:**  
     - Pagination retrieves full datasets; tests simulate multi-page responses.  
     - Logs include page numbers and counts.  

---

### Story 1.3: Implement Authentication & Error Handling  
- **Summary:**  
  As a developer, I want robust authentication and error handling for both LLM and Jira APIs, so system reliability is ensured under failure conditions.  
- **Acceptance Criteria:**  
  - Support Jira Basic Auth & OAuth; LLM API keys.  
  - Retries on 429/5xx with exponential backoff; clear error messages surfaced.  

#### Sub-tasks  
1. **Configure Authentication Mechanisms**  
   - **Description:**  
     Implement Jira Basic Auth and OAuth2 flows; read LLM keys from secure storage; handle token refresh. Document flows.  
   - **Definition of Done:**  
     - Both auth flows succeed; invalid creds produce clear errors.  
     - Tests mock expired tokens and verify refresh logic.  

2. **Add Retry & Backoff Logic**  
   - **Description:**  
     Use `tenacity` to retry on transient errors (429, 5xx) up to 3 attempts with exponential backoff starting at 1s; make retries configurable via environment variables.  
   - **Definition of Done:**  
     - Retries occur with logs reflecting attempts; tests simulate failures and assert behavior.  

3. **Centralize Error Logging**  
   - **Description:**  
     Implement a decorator that logs structured error details (`endpoint`, `payload`, `status_code`) in JSON, then re-raises or wraps exceptions.  
   - **Definition of Done:**  
     - JSON-formatted error logs include `error_type`, `timestamp`.  
     - Tests verify decorator captures and logs errors correctly.  

---

### Story 1.4: Configure Logging & Monitoring  
- **Summary:**  
  As a developer, I want structured logging and basic monitoring for API interactions, so we can track system health and performance.  
- **Acceptance Criteria:**  
  - JSON-formatted logs include `timestamp`, `level`, `endpoint`, `duration_ms`.  
  - `/metrics` endpoint exposes Prometheus counters and histograms.  

#### Sub-tasks  
1. **Implement Structured Logging**  
   - **Description:**  
     Use `structlog` for JSON logs; wrap API calls to log entry/exit, excluding sensitive data.  
   - **Definition of Done:**  
     - Logs are emitted in valid JSON; sample logs provided.  
     - Tests parse logs to verify schema compliance.  

2. **Instrument Metrics Collection**  
   - **Description:**  
     Use `prometheus_client` to define counters for requests and histograms for latency; expose `/metrics`.  
   - **Definition of Done:**  
     - Metrics endpoint returns valid Prometheus format; tests scrape and verify metrics.  

3. **Update Documentation**  
   - **Description:**  
     Add “Observability” section to README with logging and metrics setup, including sample `prometheus.yml`.  
   - **Definition of Done:**  
     - README updated with clear instructions and examples.  

---

## Epic 2: AI-Driven Backlog Analysis & Automated Ticket Management  
**Goal:** Provide intelligent analysis of backlog items, hierarchical reporting, and end-to-end automation for creating and documenting Jira tickets.

### Story 2.1: Fetch and Filter Backlog Items  
- **Summary:**  
  As a product owner, I want to fetch all Epics, Stories & Tasks (or filter by label, assignee, etc.), so that I can review and focus on relevant backlog items.  
- **Acceptance Criteria:**  
  - CLI/function accepts `--label`, `--assignee`, `--status` flags and outputs JSON.  
  - Invalid filters yield descriptive errors; tests cover edge cases.  

#### Sub-tasks  
1. **Define Filter Parameter Schema**  
   - **Description:**  
     Create a JSON schema defining allowed filter fields (`labels`, `assignee`, `status`) and types.  
   - **Definition of Done:**  
     - Schema file exists and is used for input validation.  
     - Invalid inputs are rejected with clear messages.  

2. **Implement Filtered Fetch Methods**  
   - **Description:**  
     Extend Jira client to apply filters to JQL queries, handling multiple values and sanitization.  
   - **Definition of Done:**  
     - Filtered fetch returns correct subsets; tests verify combinations.  

3. **Create CLI/Function Interface**  
   - **Description:**  
     Provide a `jira-fetch` CLI with flags for filters, help text, and examples; parse into filter schema.  
   - **Definition of Done:**  
     - CLI works as documented; invalid flags produce usage errors.  

---

### Story 2.2: Generate Hierarchical Backlog Reports  
- **Summary:**  
  As a product owner, I want a hierarchical report grouping Epics → Stories → Tasks, so that I can visualize project structure at a glance.  
- **Acceptance Criteria:**  
  - JSON and Markdown outputs correctly represent the hierarchy with Jira links.  
  - Orphans and edge cases handled gracefully; tests validate outputs.  

#### Sub-tasks  
1. **Implement Hierarchy Builder**  
   - **Description:**  
     Assemble flat issue list into nested structure, logging inconsistencies.  
   - **Definition of Done:**  
     - `build_hierarchy()` returns correct tree for test datasets; tests cover orphans.  

2. **Create JSON Formatter**  
   - **Description:**  
     Serialize hierarchy to JSON matching `hierarchy-schema.json`, including `key`, `summary`, and `url`.  
   - **Definition of Done:**  
     - Output validates against schema; integration test parses back correctly.  

3. **Create Markdown Formatter**  
   - **Description:**  
     Render Markdown report with headings and nested lists, escaping special characters and hyperlinking keys.  
   - **Definition of Done:**  
     - `report.md` matches expected format in sample and renders on GitHub.  

---

### Story 2.3: Parse Plain-Text Requirements into Ticket Structure  
- **Summary:**  
  As a product owner, I want to input new requirements in plain text, so that the assistant can generate corresponding Epics, Stories, and Sub-tasks automatically.  
- **Acceptance Criteria:**  
  - LLM prompt template yields valid JSON.  
  - Parsing and validation reject malformed outputs; tests cover failure modes.  

#### Sub-tasks  
1. **Design LLM Prompt Template**  
   - **Description:**  
     Craft prompt with examples of free-text → JSON mapping, enforcing strict output structure.  
   - **Definition of Done:**  
     - `ticket_generation_prompt.txt` contains clear examples; peer-reviewed.  

2. **Implement Parsing & Validation**  
   - **Description:**  
     Send prompt via LangChain, parse JSON into Pydantic models, surface validation errors.  
   - **Definition of Done:**  
     - Invalid or missing fields raise `ValidationError`; tests mock LLM outputs.  

3. **Write Unit Tests with Mock LLM**  
   - **Description:**  
     Use pytest and mocks to simulate valid and invalid LLM JSON responses, verifying parser behavior.  
   - **Definition of Done:**  
     - Tests cover valid, missing, and extra-field scenarios; all behave as expected.  

---

### Story 2.4: Automated Jira Ticket Creation  
- **Summary:**  
  As a product owner, I want the assistant to create Jira items via the API, so that tickets are added automatically.  
- **Acceptance Criteria:**  
  - Epics → Stories → Sub-tasks created in order with correct links.  
  - Duplicate detection skips existing items; errors retried or surfaced.  

#### Sub-tasks  
1. **Implement Ticket Creation Service**  
   - **Description:**  
     Translate JSON definitions into Jira POST payloads, log sanitized requests/responses.  
   - **Definition of Done:**  
     - Mock server returns created keys; tests handle success and HTTP errors.  

2. **Handle Parent-Child Linking**  
   - **Description:**  
     Capture Epic keys, set `Epic Link` on Stories and `parent` on Sub-tasks; implement transactional rollback or compensation.  
   - **Definition of Done:**  
     - In tests, child issues appear under correct parent; linking failures yield clear errors.  

3. **Implement Duplicate Detection**  
   - **Description:**  
     Query Jira for existing issues with same summary/type under the same parent; skip creation if found.  
   - **Definition of Done:**  
     - Service logs “Skipping duplicate”; tests confirm no duplicate API calls.  

---

### Story 2.5: Maintain Markdown Summary File  
- **Summary:**  
  As a product owner, I want the assistant to update a Markdown summary of Jira items after ticket creation, so documentation stays current.  
- **Acceptance Criteria:**  
  - Summary file updates automatically post-creation.  
  - Hierarchy and links are correct; tests validate content.  

#### Sub-tasks  
1. **Develop Markdown Generator Module**  
   - **Description:**  
     Read Jira hierarchy, render full or incremental Markdown, support header and indentation config.  
   - **Definition of Done:**  
     - Unit tests compare generated Markdown to snapshots.  

2. **Integrate Summary Update into Workflow**  
   - **Description:**  
     Hook into post-creation workflow to regenerate or append summary; log errors without interrupting ticket creation.  
   - **Definition of Done:**  
     - Integrated tests show summary file updated; failures are logged only.  

3. **Implement File Persistence Logic**  
   - **Description:**  
     Save or commit the Markdown file to a configurable location (local or Git), with optional dry-run mode that outputs diffs.  
   - **Definition of Done:**  
     - File writes or commits succeed in tests; dry-run prints correct diff.  

---

## Epic 3: Chatbot & IDE Integration Layer  
**Goal:** Expose a single, DRY Jira integration wrapper that can be invoked by both the conversational chatbot and the IDE’s AI coding assistant (via the MCP server) without duplicating API logic.

### Story 3.1: Shared Jira Integration for Chatbot & IDE  
- **Summary:**  
  As an end user, I want the chatbot to call Jira for conversational queries and the AI coding assistant in my IDE (via the MCP server) to fetch Jira ticket data—both using the same underlying integration—so that we maintain a single code path without duplication.  
- **Acceptance Criteria:**  
  1. The chatbot’s NLU/intent classifier recognizes at least three Jira-related intents (e.g., “show ticket,” “update status,” “list my tasks”) and routes them to `jira_tool(...)` without any new Jira API code written for the chatbot.  
  2. A `POST /mcp/jira-fetch` with a valid body (`{ "issue_key": "PROJ-123", "action": "get" }`) triggers exactly one call to `jira_tool("PROJ-123", action="get", payload={})` and returns the ticket JSON.  
  3. Both chatbot unit tests and MCP integration tests use a mocked `jira_client`; they assert that every Jira request—regardless of origin—goes through the same wrapper function `jira_tool`.  
  4. Unauthorized or malformed MCP requests return 401 or 400 with a clear JSON error body. Transient 5xx or 429 responses from `jira_client` trigger up to two retries before surfacing a failure.  

#### Sub-tasks  
1. **Extend Chatbot Agent to Invoke Shared `jira_tool`**  
   - **Description:**  
     Update the LangChain agent’s prompt templates and NLU routing so that any user utterance containing Jira keywords (e.g., “ticket,” “issue,” “PROJ-123”) or action verbs (e.g., “close,” “comment,” “assign”) extracts `issue_key` and `action` and then calls the new `jira_tool(...)` wrapper. This wrapper must internally call `jira_client.get_ticket(...)` or `jira_client.update_ticket(...)` without duplicating HTTP or JQL logic.  
     Adjust the agent’s code so that, upon receiving the `jira_tool` result (ticket JSON), it formats a conversational response (e.g., “PROJ-123 is currently In Progress”).  
   - **Definition of Done:**  
     - Agent NLU tests confirm that at least three Jira-related intents are recognized with ≥90% accuracy in mocks.  
     - `jira_tool` calls into `jira_client.get_ticket()`/`jira_client.update_ticket()` exactly—no low-level HTTP code in agent.  
     - A sample chatbot interaction in unit tests (“What’s the status of PROJ-123?”) results in exactly one call to `jira_tool("PROJ-123", action="get")` and returns the correct JSON response.  

2. **Implement MCP Server Endpoint to Call Shared `jira_tool`**  
   - **Description:**  
     Create a new route in the MCP server (e.g., `POST /mcp/jira-fetch`) that accepts a JSON body `{ "issue_key": "...", "action": "get" }`. The route handler must verify an `MCP_API_KEY` from headers or `.env`, then call `jira_tool(issue_key, action, {})`, and return the ticket JSON to the IDE’s AI coding assistant.  
     Handle error scenarios—such as invalid or missing `MCP_API_KEY`, malformed JSON, or `jira_client` returning 4xx/5xx—by returning a structured JSON error (including `error_code` and `message`) and applying a retry on 5xx/429 up to two attempts.  
   - **Definition of Done:**  
     - A `POST /mcp/jira-fetch` with valid credentials and body triggers exactly one invocation of `jira_tool` (confirmed by mocking `jira_client`) and returns 200 with the ticket JSON.  
     - Requests with missing/invalid `MCP_API_KEY` return HTTP 401 with `{ "error_code": "unauthorized", "message": "Invalid API key" }`.  
     - If `jira_client` first returns a 500, then a 200, the MCP endpoint retries once, and returns 200 on the second attempt. Tests simulate these scenarios.  

3. **Add Unit & Integration Tests for Chatbot vs. MCP Paths**  
   - **Description:**  
     Write unit tests (in `packages/api/tests/`) that mock `jira_client` and verify that—when the chatbot receives “Show me PROJ-123”—it calls `jira_tool("PROJ-123", action="get")`. Separately, write integration tests that spin up a mocked MCP server and simulate a `POST /mcp/jira-fetch` call, confirming one `jira_tool` invocation.  
     Ensure tests cover both “happy path” (200) and failure paths (401, 500 → retry).  
   - **Definition of Done:**  
     - `test_chatbot_jira_tool.py` has at least one scenario: “chatbot asks status” → mock `jira_client` returns a ticket; assert exactly one wrapper call and correct return.  
     - `test_mcp_jira_fetch.py` includes: valid request → one wrapper call; missing API key → 401; 500 → retry → 200. All tests pass in CI.  

