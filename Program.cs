using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using ModelContextProtocol.Server;
using System.ComponentModel;

var builder = Host.CreateApplicationBuilder(args);

// CRITICAL: MCP uses Stdout for JSON-RPC messages. 
// All application logs MUST go to Stderr to avoid corrupting the protocol.
builder.Logging.AddConsole(options =>
{
    options.LogToStandardErrorThreshold = LogLevel.Trace;
});

// Register the MCP server and the Stdio transport
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();

var app = builder.Build();
await app.RunAsync();

//AI Tools defined
[McpServerToolType]
public static class GreetingTools
{
    [McpServerTool(Name = "get_greeting"), Description]
    public static string GetGreeting(string name)
    {
        return $"Hello, {name}! Your C# server is online and ready";
    }
}
