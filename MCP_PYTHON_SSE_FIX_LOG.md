# Investigation: Python MCP Client SSE Connection Issues

## Issue
When attempting to run the Python LangGraph MCP gateway client using `python3 gateway-agent.py spring`, a `NotImplementedError` was thrown. The stack trace indicated that `MultiServerMCPClient` could not be used as an asynchronous context manager (`async with`):

```text
NotImplementedError: As of langchain-mcp-adapters 0.1.0, MultiServerMCPClient cannot be used as a context manager (e.g., async with MultiServerMCPClient(...)). Instead, you can do one of the following:
1. client = MultiServerMCPClient(...)
   tools = await client.get_tools()
```

Furthermore, the user opted to continue using **SSE Transport** instead of the `stdio` pipeline due to console logging from Spring Boot interfering with the JSON-RPC parsing across standard output.

## Root Causes

1. **Python Client API Changes**: The `langchain_mcp_adapters` package upgraded its initial abstractions in minor release `v0.1.0`. It removed the ability to handle `MultiServerMCPClient` configurations inline via `await client.connect_sse(...)` inside an asynchronous `with` block context manager.
2. **Spring Boot Transport Dependency**: The Spring Boot code and corresponding dependencies were defaulted to use standard in/out (`stdio`), so to pivot back to Server-Sent Events (SSE), standard Web MVC infrastructure had to be spun back up.

## Resolution Steps

### 1. Spring Boot Web Configuration (Server-Side)
To fully swap Spring AI's Model Context Protocol server from `stdio` transport back to HTTP (SSE), two layers had to be updated:

* **Dependency Update**: In `SpringMcpServer/pom.xml`, the existing `spring-ai-starter-mcp-server` was replaced explicitly with the web variant `spring-ai-starter-mcp-server-webmvc`.
* **Application Properties**: The target `application.properties` was fundamentally inverted. `web-application-type=none` was stripped, substituted with `servlet` and strict declarations for the SSE transport layer:
  ```properties
  server.port=8080
  spring.ai.mcp.server.transport=webmvc
  spring.main.web-application-type=servlet
  ```

### 2. Python Client Migration (Client-Side)
With the server prepared, the Python implementation inside `gateway-agent.py` was refactored to align with the new `v0.1.0` syntax for defining clients through dictionaries at instantiation, omitting the deprecated context managers:

```python
# Old broken code
# async with MultiServerMCPClient() as client:
#     await client.connect_sse("http://localhost:8080/sse")

# New v0.1.0 syntax
client = MultiServerMCPClient({
    "server": {
        "transport": "sse",
        "url": "http://localhost:8080/sse"
    }
})
```

## Result
With these adjustments matching both frameworks to SSE networking and updating the Langchain SDK patterns, the handshake completed successfully. The tools (like `get_greeting`) were dynamically read from the running Spring MVC application, enabling the Gemini model to accurately process the prompt and return the custom string back across the SSE bridge!