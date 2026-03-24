# Investigation: Spring AI Nullness ClassDefFoundError

## Issue
When attempting to run the Spring Boot application using `./mvnw spring-boot:run`, the startup failed with the following error:
```text
Caused by: java.lang.NoClassDefFoundError: org/springframework/core/Nullness
        at org.springframework.ai.util.json.schema.SpringAiSchemaModule.checkRequired(SpringAiSchemaModule.java:110)
```
This error occurred during the creation of the `getGreetingTool` bean (`FunctionToolCallback`), signaling a missing class in the dependency tree.

## Investigation Steps

1. **Verify the Dependency Tree**:
   * Evaluated `pom.xml` and identified the key versions being used: Spring Boot `3.4.2` parent and Spring AI `2.0.0-M3`.
   * Checked the Maven dependency tree which revealed `spring-core` was resolving to `v6.2.2` (linked to Spring Boot 3.4.2).

2. **Explore Spring Boot Upgrades**:
   * Attempted to upgrade the `spring-boot-starter-parent` to newer stable patched releases (e.g. `3.4.3`) to see if the `Nullness` class was introduced in slightly newer versions of the Spring framework.
   * `spring-core:6.2.3` still did not include the explicitly demanded `org.springframework.core.Nullness` class.

3. **Identify Root Cause**:
   * `2.0.0-M3` is a **Milestone** release. Milestone releases of Spring AI often build against pre-releases or very specific new versions of the Spring Framework, meaning it expects API surfaces that are sometimes unavailable or refactored out in standard, stable Spring Boot parent starters.
   * `org.springframework.core.Nullness` was used internally by the JSON Schema generation in `spring-ai-model-2.0.0-M3` but dropped or refactored away in normal releases. 

4. **Seek Downgrade Path**:
   * Checked the Maven central repository for `spring-ai-bom` and `spring-ai-starter-mcp-server` to find the most recent **stable** release. 
   * Identified `1.1.3` as the latest robust baseline.
   * Confirmed via the Maven Registry that the `spring-ai-starter-mcp-server` library existed for the `1.1.3` series.

5. **Test and Verify Resolution**:
   * Reverted the Spring Boot version to the desired `3.4.2`.
   * Swapped the `<spring-ai.version>` property from `2.0.0-M3` to `1.1.3`.
   * Ran `./mvnw clean spring-boot:run` to clear the cache and verify application startup. It succeeded cleanly without `NoClassDefFoundError` faults.

## Resolution
The `spring-ai.version` property was changed to `1.1.3`. This stable release perfectly aligns with the `v6.2.2` Spring Core classes used by the `3.4.2` Spring Boot parent, allowing seamless creation of the `FunctionToolCallback` proxies and ensuring reliable MCP server operation.