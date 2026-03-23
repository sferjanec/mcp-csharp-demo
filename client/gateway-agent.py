import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
import sys

SERVERS = {
    "dotnet": {
        "command": "dotnet",
        "args": ["run", "--project", "../TestMcpServer/TestMcpServer.csproj"]
    },
    "spring": {
        "command": "mvnw",
        "args": ["spring-boot:run"],
        "cwd": os.path.join([PARENT_DIR], "../SpringMcpServer")
    }
}

target = sys.argv[1] if len(sys.argv) > 1 else "dotnet"
config = SERVERS.get(target, SERVERS["dotnet"])

print(f"--- Starting MCP Gateway using {target.upper()} backend ---")

load_dotenv()

# Use your specific Project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

async def run_gateway():
    #1. set up the MultiServerMCPClient
    client = MultiServerMCPClient({
        "HelloServer": {
            "command": config["command"],
          "args": config["args"],
          "transport": "stdio"    
        }
    })

    #2. Load the tools from the C# server
    mcp_tools = await client.get_tools()
    print(f"Discovered tools: {[t.name for t in mcp_tools]}")

    #3. Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        project=PROJECT_ID,
        location=LOCATION
    )

    #4. Create the agent
    agent = create_agent(model=llm, tools=mcp_tools)

    #5. Execute the agent
    query = "Ask the TestServer to greet George Costanza"
    print(f"\nUser: {query}")
    
    inputs = {"messages": [{"user": query}]}

    async for event in agent.astream({"messages": [("user", query)]}):
        for value in event.values():
            content = value["messages"][-1].content
            if content:
                print(f"Assistant: {content}")



if __name__ == "__main__":
    asyncio.run(run_gateway())
