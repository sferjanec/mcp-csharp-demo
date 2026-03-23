package com.costanza.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ai.tool.function.FunctionToolCallback;

@SpringBootApplication
public class McpServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }

    public record GreetingInput(String name) {}

    @Bean
    public FunctionToolCallback getGreetingTool() {
        return FunctionToolCallback.builder("get_greeting", (GreetingInput input) -> {
                String name = input.name();
                return "Hello " + (name != null ? name : "User") + "! This greeting is served fresh from Spring Boot via manual tool callback.";
            })
            .description("Returns a friendly greeting from the Spring Boot backend")
            .inputType(GreetingInput.class)
            .build();
    }
}
