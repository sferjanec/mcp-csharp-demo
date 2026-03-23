# Spring AI MCP Tools Configuration Guide (v2.0.0-M3)

With the release of Spring AI 2.0.0-M3, the Model Context Protocol (MCP) tool registration has been heavily streamlined, converging with Spring AI's core tool execution APIs. The manual `McpSchema.Tool` and `ToolRegistration` methods have been removed.

You now have two primary ways to register tools for the Spring AI MCP Server: **Declarative** (using the `@Tool` annotation) and **Programmatic** (using `FunctionToolCallback`).

---

## 1. The Declarative Approach: `@Tool` Annotation

This is the simplest and recommended method for static tools. By adding the `@Tool` annotation to a standard method, Spring Boot's auto-configuration will automatically scan, deduce the JSON Schema from the method's arguments, and register it with the MCP Server.

### Example:
```java
package com.costanza.gateway;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.ai.tool.annotation.Tool;

@SpringBootApplication
public class McpServerApplication {

    /**
     * This registers your Java method as an MCP Tool.
     * The description and parameter names are automatically mapped to the MCP JSON Schema.
     */
    @Tool(description="Returns a friendly greeting from the Spring Boot backend")
    public String get_greeting(String name) {
        return "Hello " + (name != null ? name : "User") + "! This greeting is served fresh from Spring Boot.";
    }
}
```

**Pros:**
* Minimal boilerplate.
* Highly readable and clean.
* Spring AI automatically builds the JSON schema from your method signature.

---

## 2. The Programmatic Approach: `FunctionToolCallback`

For dynamic tools, or when you want more granular control over the tool's behavior and manual schema definitions, you can register `FunctionToolCallback` beans in the Spring Application Context. Spring's MCP Server auto-configuration automatically finds these beans and makes them available globally as MCP tools.

### Example:
```java
package com.costanza.gateway;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ai.tool.function.FunctionToolCallback;

@SpringBootApplication
public class McpServerApplication {

    // 1. Define a class or record to represent your JSON schema input
    public record GreetingInput(String name) {}

    // 2. Define the callback and return it as a bean.
    @Bean
    public FunctionToolCallback getGreetingTool() {
        return FunctionToolCallback.builder("get_greeting", (GreetingInput input) -> {
                String name = input.name();
                return "Hello " + (name != null ? name : "User") + "! This greeting is served via manual tool callback.";
            })
            .description("Returns a friendly greeting from the Spring Boot backend")
            .inputType(GreetingInput.class) // Links the schema using your record
            .build();
    }
}
```

**Pros:**
* Highly flexible—ideal if tool availability depends on runtime conditions or external configurations.
* Clearer separation of input schemas using dedicated POJOs/Records.
* Leverages standard Spring `@Bean` management.

---

### Summary
* **Use `@Tool`** when you have a static utility method and want to build functions quickly without boilerplate.
* **Use `FunctionToolCallback`** if you need to generate tools at runtime, dynamically alter their descriptions/schemas, or integrate tightly with complex Spring Bean configurations.

---

## 3. Notable Integration Notes (Spring AI 2.0.0-M3+)

### Unification with core Spring AI APIs
Earlier versions of the Spring MCP library maintained a distinct class structure for MCP tools (such as `McpSchema.Tool` and `ToolRegistration`). In the `2.0.0-M3` release, these structures were completely removed and unified into the core Spring AI `ToolCallback` and `@Tool` APIs. This means any tool you expose to your MCP clients can also be used equivalently by the Spring AI orchestrators natively.

### Spring Auto-Configuration
When you include the `spring-ai-starter-mcp-server` dependency, the framework bootstraps your MCP Server using standard Spring auto-configuration.
- By defining properties in `application.properties`/`application.yml`, you dictate how the server binds (e.g., standard input/output using Stdio vs. an SSE transport configuration).
- The `McpServerAutoConfiguration` heavily depends on you registering tools via standard beans or annotations—it scours the Spring `ApplicationContext` for any `ToolCallback` beans or methods tagged with `@Tool`, registers them systematically to the `McpServer`, and handles mapping the internal data models to standard JSON-RPC structures under the hood.