# MCP Agentic Gateway: .NET & Python Bridge

This repository demonstrates a **Model Context Protocol (MCP)** architecture that bridges a high-performance **C# (.NET 10)** backend with an intelligent **Python** AI agent powered by **Google Gemini**.


## 🏗️ Architecture Overview
The project serves as an **Agentic Microservice Gateway**. It allows an AI agent to act as an orchestrator, discovering and executing tools defined in decoupled microservices across different tech stacks (.NET and JVM).

* **Server (.NET 10):** A C# console application using the `Microsoft.ModelContextProtocol` SDK. It exposes native functions (Tools) to the protocol.
* **Client (Python 3.12):** A LangChain-powered agent that uses `langchain-mcp-adapters` to dynamically discover C# tools and invoke them based on natural language intent.
* **AI Orchestrator:** Google Gemini (via Vertex AI/Generative AI SDK) providing the decision-making logic.

---

## 🚀 Getting Started

### Prerequisites
* [.NET 10 SDK](https://dotnet.microsoft.com/download)
* [Python 3.12+](https://www.python.org/downloads/)
* [Google Cloud Project](https://console.cloud.google.com/) with Generative AI API enabled.

### 1. Configure Environment
Create a `.env` file in the `client/` directory:
```text
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

For .NET:
`cd TestMcpServer && dotnet build`

For Spring Boot:
`cd spring-mcp-server && ./mvnw clean package`

Run the Agent (with Service Switching)
The Python client is adaptable. You can specify which backend the agent should "talk" to:

`# To use the C#/.NET backend:
python gateway-agent.py dotnet

# To use the Java/Spring Boot backend:
python gateway-agent.py spring
`

