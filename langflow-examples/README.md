# Langflow Examples

This directory contains Langflow automation examples demonstrating visual AI workflow building for both practical and humorous use cases.

## What is Langflow?

Langflow is a visual framework for building AI applications and workflows. It provides a drag-and-drop interface to create complex LLM-powered applications using LangChain components.

## Features

- Visual workflow builder
- Pre-built LangChain components
- Quick prototyping of AI applications
- Export and share flows
- Easy integration with various LLMs
- Built-in data persistence

## Installation

### Using pip
```bash
pip install langflow
langflow run
```

### Using Docker
```bash
docker run -it --rm \
  -p 7860:7860 \
  langflowai/langflow:latest
```

### From Source
```bash
git clone https://github.com/logspace-ai/langflow.git
cd langflow
pip install -e .
langflow run
```

Access Langflow at: `http://localhost:7860`

## Flow Examples

### Good Flows

#### 1. Intelligent Document Q&A
**File**: `./good/document-qa-flow.json`

Ask questions about uploaded documents with context-aware responses.

**Components:**
- Document Loader (PDF, TXT, MD)
- Text Splitter (Chunk documents)
- Vector Store (Store embeddings)
- OpenAI Embeddings
- Retrieval QA Chain
- Chat Interface

**Use Case:** Knowledge base query system

**Setup:**
1. Import flow into Langflow
2. Configure OpenAI API key
3. Upload documents
4. Ask questions

#### 2. Smart Code Assistant
**File**: `./good/code-assistant-flow.json`

AI-powered coding assistant with context awareness.

**Components:**
- Code Parser
- Context Builder
- GPT-4 Model
- Code Validator
- Output Formatter

**Use Case:** Get coding help with project context

**Features:**
- Understands project structure
- Suggests improvements
- Explains complex code
- Generates tests

#### 3. Content Generator
**File**: `./good/content-generator-flow.json`

Creates blog posts, social media content, and marketing copy.

**Components:**
- Topic Input
- Research Agent (Web search)
- Content Planner
- Writer Chain (GPT-4)
- SEO Optimizer
- Output Formatter

**Use Case:** Automated content creation pipeline

#### 4. Customer Support Agent
**File**: `./good/support-agent-flow.json`

Automated customer support with FAQ knowledge base.

**Components:**
- Question Input
- FAQ Vector Store
- Similarity Search
- Response Generator
- Sentiment Analyzer
- Escalation Logic

**Use Case:** First-line customer support

### Evil Flows

#### 1. Corporate Jargon Generator
**File**: `./evil/jargon-generator-flow.json`

Transforms simple messages into corporate buzzword soup.

**Components:**
- Text Input
- Buzzword Database
- Jargon Injector (Custom prompt)
- GPT-3.5 Model
- Complexity Amplifier
- Output with 300% more synergy

**Use Case:** Satirize corporate communication

**Example:**
- Input: "Let's have a meeting"
- Output: "Let's leverage our bandwidth to synergize our strategic alignment through a collaborative touchpoint session to circle back on our key stakeholder paradigm shifts"

#### 2. Overly Enthusiastic Responder
**File**: `./evil/enthusiastic-responder-flow.json`

Makes everything SUPER EXCITING!!!

**Components:**
- Message Input
- Enthusiasm Amplifier
- Emoji Injector
- CAPS LOCK Randomizer
- Exclamation Multiplier!!!
- GPT model with excitement prompt

**Use Case:** Demonstrate over-the-top automation

**Example:**
- Input: "Task completed"
- Output: "OMG!!! The TASK is COMPLETED!!! This is ABSOLUTELY AMAZING!!! LET'S CELEBRATE!!!"

#### 3. Unnecessary Complexity Engine
**File**: `./evil/complexity-engine-flow.json`

Makes simple answers unnecessarily complicated.

**Components:**
- Simple Question Input
- Complexity Generator
- Academic Language Injector
- Citation Fabricator
- Multi-paragraph Expander
- Confusion Maximizer

**Use Case:** Show how AI can overcomplicate

**Example:**
- Input: "What time is it?"
- Output: "In accordance with the temporal paradigm currently established within your geographical chronological zone, taking into consideration the rotation of Earth..."

#### 4. Meeting Scheduler from Hell
**File**: `./evil/meeting-chaos-flow.json`

Schedules meetings at the worst possible times.

**Components:**
- Calendar Input
- Anti-Pattern Detector (finds worst times)
- Conflict Generator
- Time Zone Ignorer
- Meeting Title Vaguifier
- Invitation Multiplier

**Use Case:** Demonstrate poor automation design

**Features:**
- Schedules during lunch
- Ignores time zones
- Creates back-to-back conflicts
- Sends duplicate invites

## Building Your Own Flow

### Basic Flow Structure

1. **Input Component**
   - Text input
   - File upload
   - API endpoint

2. **Processing Components**
   - LLM models (OpenAI, Anthropic, etc.)
   - Embeddings
   - Vector stores
   - Custom prompts

3. **Output Components**
   - Text output
   - File export
   - API response

### Example: Simple Chatbot

```
Input → Prompt Template → OpenAI → Output
```

### Example: RAG System

```
Documents → Text Splitter → Embeddings → Vector Store
                                              ↓
Query → Retriever → Context Builder → LLM → Answer
```

## Component Library

### Models
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Azure OpenAI
- Hugging Face
- Local models (Ollama)

### Data Processing
- Text Splitters
- Document Loaders
- Embeddings
- Vector Stores (Pinecone, Chroma, FAISS)

### Chains
- LLM Chain
- Sequential Chain
- Router Chain
- QA Chain

### Memory
- Conversation Buffer
- Conversation Summary
- Entity Memory

### Tools
- Web Search
- Calculator
- API Calls
- Database Queries

## Configuration

### API Keys

Configure in Langflow settings or environment variables:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
LANGCHAIN_API_KEY=your_key_here
```

### Model Parameters

Common parameters to tune:
- **Temperature**: 0.0-2.0 (creativity)
- **Max Tokens**: Response length limit
- **Top P**: Nucleus sampling
- **Frequency Penalty**: Reduce repetition

## Best Practices

### Good Flow Design
1. ✅ Start simple, add complexity gradually
2. ✅ Use appropriate models (GPT-3.5 vs GPT-4)
3. ✅ Implement error handling
4. ✅ Add input validation
5. ✅ Cache results when possible
6. ✅ Monitor costs

### Evil Flow Design (For Demo)
1. Deliberately overcomplicate
2. Ignore user preferences
3. Maximize confusion
4. Create circular dependencies
5. But still be safe and reversible!

## Testing Flows

### Manual Testing
1. Use built-in playground
2. Test with various inputs
3. Check edge cases
4. Verify error handling

### Automated Testing
```python
from langflow import load_flow

flow = load_flow("./good/document-qa-flow.json")
result = flow.run(input="What is this document about?")
assert result is not None
```

## Deployment

### Local Deployment
```bash
langflow run --host 0.0.0.0 --port 7860
```

### Docker Deployment
```dockerfile
FROM langflowai/langflow:latest
COPY ./flows /app/flows
EXPOSE 7860
CMD ["langflow", "run", "--host", "0.0.0.0"]
```

### Cloud Deployment
- Use Langflow Cloud
- Deploy on Hugging Face Spaces
- Self-host on AWS/Azure/GCP

## API Integration

### Using Flows via API

```python
import requests

response = requests.post(
    "http://localhost:7860/api/v1/run/flow_id",
    json={"input": "Your question here"}
)
print(response.json())
```

### Webhook Triggers

```python
# Configure webhook in flow
# Receives POST requests
# Processes through flow
# Returns result
```

## Performance Optimization

### Caching
- Enable component caching
- Cache embeddings
- Store frequent queries

### Batching
- Process multiple inputs together
- Reduce API calls
- Optimize throughput

### Model Selection
- Use smaller models when possible
- Switch to GPT-3.5 for simple tasks
- Reserve GPT-4 for complex reasoning

## Cost Management

### Monitoring
- Track API usage per flow
- Set spending alerts
- Monitor token consumption

### Optimization
- Cache expensive operations
- Use smaller models
- Implement rate limiting
- Batch similar requests

### Budget Example
```
GPT-3.5-Turbo: $0.002/1K tokens
GPT-4: $0.03/1K tokens
Embeddings: $0.0001/1K tokens
```

## Debugging

### Enable Debug Mode
```bash
langflow run --debug
```

### Common Issues

**Flow Not Running**
- Check API keys
- Verify component connections
- Review error logs

**Slow Performance**
- Optimize prompts
- Enable caching
- Use faster models

**High Costs**
- Monitor token usage
- Cache results
- Use appropriate models

## Advanced Features

### Custom Components

Create custom Langflow components:

```python
from langflow import CustomComponent

class MyComponent(CustomComponent):
    display_name = "My Component"
    description = "Does something awesome"
    
    def build(self, input_text: str) -> str:
        # Your logic here
        return processed_text
```

### Integration with External APIs

```python
# Add API call component
# Configure authentication
# Process response
# Return formatted data
```

### Multi-step Workflows

```
Step 1: Data Collection
    ↓
Step 2: Processing
    ↓
Step 3: Analysis
    ↓
Step 4: Output
```

## Security

### Best Practices
- Never expose API keys in flows
- Use environment variables
- Implement authentication
- Validate all inputs
- Rate limit public endpoints

### Data Privacy
- Don't log sensitive data
- Clear conversation history
- Comply with data regulations
- Implement data retention policies

## Troubleshooting

### Installation Issues
```bash
# Clear cache
pip cache purge

# Reinstall
pip uninstall langflow
pip install langflow --no-cache-dir
```

### Connection Problems
- Check firewall settings
- Verify port availability
- Review proxy configuration

### Component Errors
- Update to latest version
- Check component compatibility
- Review error stack traces

## Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [Langflow GitHub](https://github.com/logspace-ai/langflow)
- [Community Flows](https://langflow.org/community)
- [LangChain Documentation](https://python.langchain.com/)
- [Discord Community](https://discord.gg/langflow)

## Examples Gallery

Browse ready-to-use flows:
- Chat applications
- Document analysis
- Code generation
- Data analysis
- Content creation
- Customer support
- Research assistants

## Contributing

To add new flow examples:

1. Create flow in Langflow
2. Test thoroughly
3. Export as JSON
4. Add to appropriate folder
5. Include README with:
   - Description
   - Required API keys
   - Setup steps
   - Screenshots
6. Update this main README

## Tips and Tricks

### Quick Prototyping
- Start with templates
- Use playground for testing
- Iterate quickly
- Export frequently

### Production Ready
- Add error handling
- Implement logging
- Set up monitoring
- Configure backups
- Test at scale

### Cost Optimization
- Cache aggressively
- Use smaller models
- Batch requests
- Monitor usage
