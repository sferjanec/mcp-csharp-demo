# 🛠️ Development Log: MCP Agentic Gateway

### Phase 1: The Protocol Bridge (Current)
* **Goal:** Establish a JSON-RPC connection between .NET 10 and Python 3.12.
* **Status:** Completed. Successfully implemented dynamic tool discovery where Gemini can "see" C# methods and invoke them via the Python client.

### Phase 2: Persistence & Containerization (In Progress)
* **Goal:** Move from hardcoded mock data to a persistent PostgreSQL store.
* **Tech:** Docker Desktop (WSL 2), EF Core, and Npgsql.
* **Focus:** Implementing a "Disaster Recovery" schema to manage insurance adjusters and resource allocation.

### Phase 3: Cross-Platform Parity (Planned)
* **Goal:** Implement the MCP Server in **Java/Spring Boot** to demonstrate protocol-level interoperability.
* **Focus:** Allowing the Python Orchestrator to switch between .NET and JVM backends seamlessly.

### Phase 4: Cloud Orchestration
* **Goal:** Deploy the entire stack to **Google Cloud Platform (GCP)**.
* **Tech:** Cloud Run (SSE Transport), Cloud SQL, and Secret Manager.

### v0.1.3 - Spring AI 2.0.0-M3 Migration
* **Issue:** Compilation failure due to package renames in the Spring AI 2.0.0-M3 release (March 2026).
* **Fix:** Migrated imports from `org.springframework.ai.mcp.spec` to the core `org.springframework.ai.mcp` package.
* **Refactor:** Simplified the `ToolRegistration` bean to use the new functional signature.

### v0.1.5 - Declarative Tool Mapping
* **Refactor:** Migrated from manual `ToolRegistration` beans to the `@Tool` annotation.
* **Benefit:** Leveraged Spring AI 2.0.0-M3's auto-configuration to handle JSON-RPC mapping and schema generation, reducing boilerplate code by 60%.
* **Status:** Java backend is now functionally at parity with the .NET [McpServerTool] implementation.

### v0.1.6 - Manual vs Declarative Tool Configuration
* **Exploration:** Investigated the updated programmatic tool registration method for Spring AI 2.0.0-M3 since the legacy `McpSchema.Tool` / `ToolRegistration` paths were completely removed.
* **Refactor:** Successfully drafted tests using `FunctionToolCallback` as a `@Bean` for manual schema mapping and tool control.
* **Status:** Both declarative (`@Tool`) and programmatic (`FunctionToolCallback`) mechanisms are fully operational and documented in a new `SPRING_AI_MCP_TOOLS.md` reference file.