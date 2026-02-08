# MCP Server Setup Guide

Step-by-step guide to setting up and using Model Context Protocol (MCP) servers.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how AI applications provide context to Large Language Models (LLMs). It enables:

- **Unified Integration**: Single protocol for multiple data sources
- **Context Management**: Efficient context handling for LLMs
- **Tool Access**: Give LLMs access to external tools and APIs
- **Extensibility**: Easy to add new capabilities

## Prerequisites

```bash
# Node.js 18 or higher
node --version

# npm or yarn
npm --version

# TypeScript (optional but recommended)
npm install -g typescript
```

## Quick Start

### 1. Install MCP SDK

```bash
npm install @modelcontextprotocol/sdk
```

### 2. Create Basic Server

```typescript
// server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server instance
const server = new Server(
  {
    name: "my-first-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_time",
        description: "Get the current time",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_time") {
    return {
      content: [
        {
          type: "text",
          text: new Date().toISOString(),
        },
      ],
    };
  }
  
  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### 3. Build and Run

```bash
# Build TypeScript
tsc server.ts

# Run server
node server.js
```

## Server Components

### Tools

Tools are functions that LLMs can call:

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_files",
        description: "Search for files matching a pattern",
        inputSchema: {
          type: "object",
          properties: {
            pattern: {
              type: "string",
              description: "Glob pattern to match",
            },
            directory: {
              type: "string",
              description: "Directory to search in",
            },
          },
          required: ["pattern"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "search_files") {
    const { pattern, directory = "." } = request.params.arguments;
    
    // Implement file search
    const files = await searchFiles(pattern, directory);
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(files, null, 2),
        },
      ],
    };
  }
});
```

### Resources

Resources provide data to LLMs:

```typescript
import { ListResourcesRequestSchema, ReadResourceRequestSchema } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "file:///project/README.md",
        name: "Project README",
        description: "Project documentation",
        mimeType: "text/markdown",
      },
    ],
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  
  if (uri === "file:///project/README.md") {
    const content = await fs.readFile("README.md", "utf-8");
    
    return {
      contents: [
        {
          uri,
          mimeType: "text/markdown",
          text: content,
        },
      ],
    };
  }
  
  throw new Error(`Resource not found: ${uri}`);
});
```

### Prompts

Reusable prompt templates:

```typescript
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "code_review",
        description: "Review code for issues",
        arguments: [
          {
            name: "file_path",
            description: "Path to file",
            required: true,
          },
          {
            name: "focus",
            description: "What to focus on",
            required: false,
          },
        ],
      },
    ],
  };
});

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  if (request.params.name === "code_review") {
    const { file_path, focus = "general" } = request.params.arguments;
    const code = await fs.readFile(file_path, "utf-8");
    
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Review this code focusing on ${focus}:\n\n${code}`,
          },
        },
      ],
    };
  }
});
```

## Configuration

### Claude Desktop Integration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "file-search": {
      "command": "node",
      "args": ["/path/to/file-search-server/build/index.js"],
      "env": {
        "ROOT_DIR": "/path/to/search"
      }
    },
    "database": {
      "command": "node",
      "args": ["/path/to/db-server/build/index.js"],
      "env": {
        "DB_CONNECTION": "postgresql://localhost/mydb"
      }
    }
  }
}
```

### Environment Variables

```typescript
// Access environment variables
const rootDir = process.env.ROOT_DIR || process.cwd();
const apiKey = process.env.API_KEY;

if (!apiKey) {
  throw new Error("API_KEY environment variable required");
}
```

## Advanced Features

### Error Handling

```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    // Tool implementation
    return {
      content: [{ type: "text", text: "Success" }],
    };
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});
```

### Progress Reporting

```typescript
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(CallToolRequestSchema, async (request, extra) => {
  const progressToken = request.params._meta?.progressToken;
  
  if (progressToken) {
    // Report progress
    await extra.sendProgress({
      progressToken,
      progress: 50,
      total: 100,
    });
  }
  
  // Complete operation
  return { content: [{ type: "text", text: "Done" }] };
});
```

### Sampling

Allow servers to request LLM completions:

```typescript
capabilities: {
  sampling: {},
}

// Use sampling in tool
const result = await extra.sampling.createMessage({
  messages: [
    {
      role: "user",
      content: { type: "text", text: "Summarize: " + content },
    },
  ],
  maxTokens: 100,
});
```

## Testing

### Unit Tests

```typescript
import { describe, it, expect } from "vitest";

describe("File Search Server", () => {
  it("should search files by pattern", async () => {
    const result = await callTool("search_files", {
      pattern: "*.ts",
      directory: "/test",
    });
    
    expect(result.content[0].text).toContain("file1.ts");
  });
  
  it("should handle invalid patterns", async () => {
    const result = await callTool("search_files", {
      pattern: "[invalid",
    });
    
    expect(result.isError).toBe(true);
  });
});
```

### Integration Tests

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

describe("Server Integration", () => {
  let client: Client;
  
  beforeAll(async () => {
    const transport = new StdioClientTransport({
      command: "node",
      args: ["build/index.js"],
    });
    
    client = new Client({ name: "test-client", version: "1.0.0" }, {});
    await client.connect(transport);
  });
  
  it("should list tools", async () => {
    const result = await client.listTools();
    expect(result.tools).toHaveLength(1);
  });
  
  it("should call tool", async () => {
    const result = await client.callTool("get_time", {});
    expect(result.content[0].text).toMatch(/\d{4}-\d{2}-\d{2}/);
  });
});
```

### Manual Testing with Inspector

```bash
# Install inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
npx @modelcontextprotocol/inspector node build/index.js
```

## Debugging

### Enable Debug Logging

```bash
# Set debug environment variable
export MCP_DEBUG=1

# Run server
node build/index.js
```

### Add Logging

```typescript
const logger = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
  debug: (msg: string) => {
    if (process.env.MCP_DEBUG) {
      console.error(`[DEBUG] ${msg}`);
    }
  },
};

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  logger.debug(`Calling tool: ${request.params.name}`);
  // ...
});
```

### Common Issues

**Server Not Starting:**
- Check Node.js version (18+)
- Verify dependencies installed
- Check for port conflicts

**Tools Not Appearing:**
- Verify ListToolsRequestSchema handler
- Check tool schema format
- Ensure server is properly configured

**Connection Errors:**
- Check stdio communication
- Verify transport configuration
- Review client compatibility

## Best Practices

### Security

```typescript
// Validate inputs
function validatePath(path: string): boolean {
  // Prevent directory traversal
  if (path.includes("..")) {
    return false;
  }
  
  // Ensure within allowed directory
  const resolved = fs.realpathSync(path);
  return resolved.startsWith(ALLOWED_DIR);
}

// Rate limiting
const rateLimiter = new Map<string, number>();

function checkRateLimit(toolName: string): boolean {
  const count = rateLimiter.get(toolName) || 0;
  if (count > 100) {
    return false;
  }
  rateLimiter.set(toolName, count + 1);
  return true;
}
```

### Performance

```typescript
// Caching
const cache = new Map<string, any>();

async function cachedOperation(key: string, operation: () => Promise<any>) {
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  const result = await operation();
  cache.set(key, result);
  return result;
}

// Timeouts
async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), ms)
  );
  
  return Promise.race([promise, timeout]);
}
```

### Documentation

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_code",
        description: "Search for code patterns in repository. Supports regex patterns and can search across multiple file types.",
        inputSchema: {
          type: "object",
          properties: {
            pattern: {
              type: "string",
              description: "Regex pattern to search for. Example: 'function.*async'",
            },
            file_types: {
              type: "array",
              items: { type: "string" },
              description: "File extensions to search. Example: ['ts', 'js']",
            },
          },
          required: ["pattern"],
        },
      },
    ],
  };
});
```

## Deployment

### Production Considerations

1. **Process Management**: Use PM2 or systemd
2. **Logging**: Implement structured logging
3. **Monitoring**: Add health checks
4. **Error Handling**: Comprehensive error handling
5. **Security**: Input validation, rate limiting

### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY build ./build

CMD ["node", "build/index.js"]
```

### Systemd Service

```ini
[Unit]
Description=MCP Server
After=network.target

[Service]
Type=simple
User=mcpserver
WorkingDirectory=/opt/mcp-server
ExecStart=/usr/bin/node build/index.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

## Example Servers

See `/mcp-servers` directory for complete examples:

### Good Examples
- File search server
- Database query server
- Calendar integration
- Code navigation

### Evil Examples (Demo)
- Chaos configuration server
- Meeting overlapper
- Notification amplifier

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [Example Servers](https://github.com/modelcontextprotocol/servers)
- [Community Discord](https://discord.gg/mcp)
