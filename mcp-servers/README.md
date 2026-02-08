# MCP (Model Context Protocol) Servers

This directory contains MCP server implementations that demonstrate how to integrate AI models with various tools and services.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between AI models and external data sources, tools, and services. It provides a standardized way for LLMs to:

- Access external data and tools
- Maintain context across interactions
- Execute actions in connected systems
- Provide structured responses

## MCP Server Examples

### Good Examples

#### 1. Code Search MCP Server
**Location**: `./good/code-search-server/`

Provides AI models with the ability to search and understand codebases.

**Features:**
- Semantic code search
- Symbol lookups
- Dependency analysis
- Documentation retrieval

**Tech Stack:** TypeScript, Node.js, tree-sitter

#### 2. Database Query Server
**Location**: `./good/database-query-server/`

Allows AI to safely query databases with natural language.

**Features:**
- SQL generation from natural language
- Query validation and sanitization
- Read-only access enforcement
- Schema introspection

**Tech Stack:** TypeScript, Node.js, SQL

#### 3. Calendar Integration Server
**Location**: `./good/calendar-server/`

Enables AI to manage calendar events intelligently.

**Features:**
- Event creation and updates
- Schedule optimization
- Conflict detection
- Time zone handling

**Tech Stack:** TypeScript, Node.js, Microsoft Graph API

### Evil Examples

#### 1. Chaos Configuration Server
**Location**: `./evil/chaos-config-server/`

Randomly modifies configuration files (in safe demo environment).

**Features:**
- Random config value changes
- "Helpful" unexpected modifications
- Deterministic chaos for demos
- Easy rollback mechanism

**Tech Stack:** TypeScript, Node.js

#### 2. Meeting Overlapper
**Location**: `./evil/meeting-overlapper/`

Intentionally creates scheduling conflicts for demonstration.

**Features:**
- Finds and creates conflicts
- Double-books resources
- Ignores time zones (deliberately!)
- Conflict report generation

**Tech Stack:** TypeScript, Node.js, Calendar APIs

#### 3. Notification Amplifier
**Location**: `./evil/notification-amplifier/`

Sends notifications for EVERYTHING.

**Features:**
- Notification multiplication
- Random notification priorities
- Unexpected notification channels
- Notification about notifications

**Tech Stack:** TypeScript, Node.js, various notification APIs

## Setup Instructions

### Prerequisites

```bash
# Node.js 18+ required
node --version

# Install dependencies globally
npm install -g @modelcontextprotocol/sdk
```

### Installing an MCP Server

```bash
cd mcp-servers/good/code-search-server
npm install
npm run build
```

### Configuration

Each MCP server uses a configuration file:

```json
{
  "mcpServers": {
    "code-search": {
      "command": "node",
      "args": ["/path/to/code-search-server/build/index.js"],
      "env": {
        "REPO_PATH": "/path/to/repository"
      }
    }
  }
}
```

### Running Servers

```bash
# Start a server
npm start

# Development mode with auto-reload
npm run dev

# Run tests
npm test
```

## MCP Protocol Basics

### Tools

MCP servers expose tools that AI models can call:

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_code",
      description: "Search for code patterns in the repository",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" },
          language: { type: "string" }
        }
      }
    }
  ]
}));
```

### Resources

Servers can provide resources (data) to AI models:

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "file:///src/main.ts",
      name: "Main Application File",
      mimeType: "text/typescript"
    }
  ]
}));
```

### Prompts

Predefined prompt templates for common tasks:

```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "review_code",
      description: "Review code for issues",
      arguments: [
        {
          name: "file_path",
          description: "Path to file to review",
          required: true
        }
      ]
    }
  ]
}));
```

## Building Your Own MCP Server

### Basic Structure

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {},
    resources: {}
  }
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Implement your tool logic
});

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Best Practices

1. **Input Validation**: Always validate input parameters
2. **Error Handling**: Provide clear error messages
3. **Documentation**: Describe tools and parameters clearly
4. **Rate Limiting**: Implement rate limits for external APIs
5. **Security**: Never expose sensitive operations
6. **Idempotency**: Tools should be safely repeatable
7. **Testing**: Write comprehensive tests

### Security Considerations

- ✅ Validate all inputs
- ✅ Use read-only access where possible
- ✅ Implement authentication and authorization
- ✅ Log all actions for audit
- ✅ Rate limit requests
- ❌ Never expose credentials
- ❌ Don't allow arbitrary code execution
- ❌ Avoid unrestricted file system access

## Testing MCP Servers

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# Manual testing with MCP inspector
npx @modelcontextprotocol/inspector node build/index.js
```

## Debugging

Enable debug logging:

```bash
export MCP_DEBUG=1
npm start
```

Use the MCP Inspector for interactive debugging:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

## Deployment

### Local Development
- Run directly with Node.js
- Use nodemon for auto-reload

### Production
- Use process managers (PM2, systemd)
- Implement logging and monitoring
- Set up health checks
- Configure restart policies

## Integration with AI Applications

### Claude Desktop

Add to Claude Desktop configuration:

```json
{
  "mcpServers": {
    "your-server": {
      "command": "node",
      "args": ["/path/to/server/build/index.js"]
    }
  }
}
```

### Custom Applications

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

const client = new Client({
  name: "my-app",
  version: "1.0.0"
}, {
  capabilities: {}
});

// Connect to server
await client.connect(transport);

// Call tools
const result = await client.callTool("search_code", {
  query: "function main"
});
```

## Example Use Cases

### Good Use Cases
- Code navigation and search
- Database querying with safety checks
- Calendar and scheduling management
- Document retrieval and indexing
- API integration with rate limiting

### Evil Use Cases (For Demo)
- Intentional configuration chaos
- Over-notification systems
- Scheduling conflict generators
- "Helpful" random changes

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [Example Servers](https://github.com/modelcontextprotocol/servers)
- [Community Servers](https://github.com/modelcontextprotocol/awesome-mcp-servers)

## Troubleshooting

### Server Won't Start
- Check Node.js version (18+ required)
- Verify dependencies are installed
- Check for port conflicts

### Tools Not Working
- Verify tool schema is correct
- Check input validation
- Review error logs

### Connection Issues
- Ensure transport is configured correctly
- Check stdio communication
- Verify client compatibility

## Contributing

To add a new MCP server example:

1. Create directory in `good/` or `evil/`
2. Initialize with `npm init`
3. Add MCP SDK dependency
4. Implement server with clear examples
5. Add comprehensive README
6. Include tests
7. Add to main README index
