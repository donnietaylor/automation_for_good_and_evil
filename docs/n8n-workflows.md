# n8n Workflows Guide

Complete guide to building and deploying n8n workflows for automation.

## Installation and Setup

### Quick Start with Docker

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access at: http://localhost:5678

### Production Setup with Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: n8n
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      DB_TYPE: postgresdb
      DB_POSTGRESDB_HOST: postgres
      DB_POSTGRESDB_PORT: 5432
      DB_POSTGRESDB_DATABASE: n8n
      DB_POSTGRESDB_USER: n8n
      DB_POSTGRESDB_PASSWORD: n8n
      N8N_ENCRYPTION_KEY: ${N8N_ENCRYPTION_KEY}
      WEBHOOK_URL: https://your-domain.com/
    volumes:
      - n8n-data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres-data:
  n8n-data:
```

### npm Installation

```bash
# Global installation
npm install -g n8n

# Start n8n
n8n start

# With custom configuration
n8n start --tunnel
```

## Core Concepts

### Nodes

Building blocks of workflows:

- **Trigger Nodes**: Start workflows (Webhook, Schedule, Email)
- **Action Nodes**: Perform operations (HTTP Request, Database)
- **Logic Nodes**: Control flow (IF, Switch, Merge)
- **Transform Nodes**: Data manipulation (Function, Set, Code)

### Workflow Execution

1. **Trigger**: Workflow starts
2. **Processing**: Nodes execute in sequence
3. **Branching**: Conditional paths
4. **Completion**: Final actions

### Data Flow

```javascript
// Each node receives items array
[
  {
    json: {
      id: 1,
      name: "Example"
    },
    binary: {}
  }
]

// Transform data
items.map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}))
```

## Building Workflows

### Example 1: Email Automation

```
Gmail Trigger
  ↓
IF Node (Check importance)
  ↓ (urgent)
  Slack Node (Send alert)
  ↓
Google Sheets (Log email)
```

**Configuration:**

1. **Gmail Trigger**
   - Enable Gmail API
   - Set label filter: "inbox"

2. **IF Node**
   - Condition: `{{$json.subject}}` contains "urgent"

3. **Slack Node**
   - Channel: #alerts
   - Message: `New urgent email from {{$json.from}}`

4. **Google Sheets**
   - Spreadsheet: Email Log
   - Add row with email data

### Example 2: API Integration

```
Webhook Trigger
  ↓
HTTP Request (External API)
  ↓
Function Node (Transform data)
  ↓
Database Insert
  ↓
Respond to Webhook
```

**Configuration:**

1. **Webhook**
   - Method: POST
   - Path: /api/process

2. **HTTP Request**
   - URL: `https://api.example.com/data`
   - Method: GET
   - Authentication: Bearer Token

3. **Function Node**
```javascript
// Transform API response
items = items.map(item => {
  const data = item.json;
  return {
    json: {
      id: data.id,
      name: data.name.toUpperCase(),
      timestamp: new Date().toISOString(),
      processed: true
    }
  };
});

return items;
```

4. **Database Insert**
   - Connection: PostgreSQL
   - Table: processed_data
   - Columns: Map from transformed data

### Example 3: Scheduled Report

```
Schedule Trigger (Daily 9 AM)
  ↓
Database Query
  ↓
Function Node (Generate report)
  ↓
OpenAI Node (Summarize)
  ↓
Email Node (Send report)
```

**Configuration:**

1. **Schedule Trigger**
   - Cron: `0 9 * * *`
   - Timezone: America/New_York

2. **Database Query**
```sql
SELECT 
  DATE(created_at) as date,
  COUNT(*) as count,
  AVG(value) as average
FROM metrics
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY DATE(created_at)
```

3. **Function Node**
```javascript
// Format data for report
const data = items[0].json;

const report = `
Daily Report - ${new Date().toLocaleDateString()}

Metrics:
- Total Items: ${data.count}
- Average Value: ${data.average.toFixed(2)}
`;

return [{
  json: { report, data }
}];
```

4. **OpenAI Node**
   - Prompt: "Summarize this report and highlight key insights: {{$json.report}}"
   - Model: gpt-3.5-turbo

5. **Email Node**
   - To: team@company.com
   - Subject: "Daily Report - {{$now.toLocaleString()}}"
   - Body: AI-generated summary

## Advanced Techniques

### Error Handling

```
Main Workflow
  ↓
[Error Workflow]
  ↓
Log Error
  ↓
Notify Team
  ↓
Retry Logic
```

**Error Workflow Configuration:**
- Trigger: On workflow error
- Capture error details
- Send to logging service
- Notify via Slack/Email
- Optional: Retry with exponential backoff

### Loops and Iterations

```javascript
// Split In Batches Node
{
  "batchSize": 10,
  "options": {
    "reset": false
  }
}

// Process batch
items.forEach(item => {
  // Process each item
  processItem(item.json);
});

// Check if more batches
if ($("SplitInBatches").context.done === false) {
  // Continue to next batch
  return items;
}
```

### Sub-Workflows

**Main Workflow:**
```
Trigger
  ↓
Execute Workflow (Data Processing)
  ↓
Execute Workflow (Send Notifications)
  ↓
Complete
```

**Benefits:**
- Reusable logic
- Better organization
- Independent testing
- Easier maintenance

### Custom Functions

```javascript
// Function Node - Utility Functions
function processData(data) {
  // Complex transformation
  return {
    id: data.id,
    normalized: normalizeString(data.name),
    validated: validateEmail(data.email),
    enriched: enrichData(data)
  };
}

function normalizeString(str) {
  return str.trim().toLowerCase().replace(/\s+/g, '_');
}

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function enrichData(data) {
  // Call external service or add computed fields
  return {
    ...data,
    score: calculateScore(data),
    category: categorize(data)
  };
}

// Process all items
return items.map(item => ({
  json: processData(item.json)
}));
```

## Integration Examples

### GitHub Integration

```
GitHub Trigger (New PR)
  ↓
OpenAI (Summarize changes)
  ↓
Slack (Notify team)
  ↓
Linear (Create review task)
```

### Slack Bot

```
Slack Trigger (Message)
  ↓
IF Node (Check command)
  ↓ (/report)
  Database Query
  ↓
Function (Format)
  ↓
Slack (Reply)
```

### Data Pipeline

```
Schedule Trigger
  ↓
HTTP Request (Fetch data)
  ↓
Filter (Valid records)
  ↓
Transform (Clean data)
  ↓
Database (Upsert)
  ↓
Slack (Summary)
```

## Best Practices

### 1. Workflow Organization

```
📁 Workflows
├── 📂 Production
│   ├── Email Processing
│   ├── Data Sync
│   └── Notifications
├── 📂 Development
│   ├── Test Email
│   └── Test API
└── 📂 Archive
    └── Old Workflows
```

### 2. Naming Conventions

- **Workflows**: `[Environment] - [Purpose]` 
  - Example: `PROD - Customer Email Automation`
- **Nodes**: Descriptive names
  - Example: "Fetch Customer Data" not "HTTP Request"

### 3. Error Handling

```javascript
try {
  // Main logic
  const result = await processData(item.json);
  return { json: result };
} catch (error) {
  // Handle error
  return {
    json: {
      error: error.message,
      item: item.json,
      timestamp: new Date().toISOString()
    },
    isError: true
  };
}
```

### 4. Performance Optimization

- **Use batching** for large datasets
- **Enable caching** for repeated operations
- **Limit API calls** with rate limiting
- **Optimize queries** in database nodes
- **Use async operations** when possible

### 5. Security

- **Environment variables** for secrets
- **Webhook authentication** for public endpoints
- **Input validation** in Function nodes
- **Rate limiting** on triggers
- **Audit logging** for sensitive operations

## Monitoring and Maintenance

### Health Checks

```
Schedule Trigger (Every 5 min)
  ↓
HTTP Request (Health endpoints)
  ↓
IF Node (Check status)
  ↓ (down)
  PagerDuty/Slack Alert
```

### Performance Monitoring

```javascript
// Add timing metrics
const startTime = Date.now();

// Your logic here
const result = await performOperation();

const duration = Date.now() - startTime;

return [{
  json: {
    result,
    metrics: {
      duration,
      timestamp: new Date().toISOString()
    }
  }
}];
```

### Logging

```javascript
// Structured logging
function log(level, message, data = {}) {
  console.log(JSON.stringify({
    level,
    message,
    data,
    workflow: $workflow.name,
    execution: $execution.id,
    timestamp: new Date().toISOString()
  }));
}

log('info', 'Processing item', { itemId: item.json.id });
```

## Troubleshooting

### Common Issues

**Workflow Not Triggering:**
1. Check trigger configuration
2. Verify webhook URL
3. Ensure workflow is activated
4. Check trigger conditions

**Node Failing:**
1. Review node configuration
2. Check credentials
3. Verify API limits
4. Review error message

**Slow Execution:**
1. Optimize database queries
2. Use batching
3. Enable caching
4. Review API response times

### Debug Mode

```bash
# Enable debug logging
export N8N_LOG_LEVEL=debug

# Start n8n
n8n start
```

### Testing Strategies

1. **Unit Testing**: Test individual nodes
2. **Integration Testing**: Test full workflows
3. **Load Testing**: Test with production-like data
4. **Error Testing**: Test error scenarios

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Community Forum](https://community.n8n.io/)
- [Workflow Templates](https://n8n.io/workflows)
- [Node Reference](https://docs.n8n.io/integrations/)
- [YouTube Channel](https://www.youtube.com/@n8n-io)

## Example Files

See `/n8n-workflows` directory for:
- Good automation examples
- Evil automation examples (for demo)
- Template workflows
- Best practice examples
