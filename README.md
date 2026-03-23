# MCP Agentic Gateway: .NET & Python Bridge

This repository demonstrates a **Model Context Protocol (MCP)** architecture that bridges a high-performance **C# (.NET 10)** backend with an intelligent **Python** AI agent powered by **Google Gemini**.

[Image of MCP architecture diagram showing a host application connecting to multiple MCP servers via JSON-RPC]

## 🏗️ Architecture Overview
The project serves as a prototype for an **Agentic Microservice Gateway**. In this pattern, the AI agent acts as a reasoning layer, discovering and executing tools defined in decoupled .NET microservices.

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