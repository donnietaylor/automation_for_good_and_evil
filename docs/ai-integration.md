# AI Integration Guide

Comprehensive guide for integrating AI capabilities into automation workflows.

## AI Services Overview

### OpenAI API
- GPT-4, GPT-3.5-Turbo models
- DALL-E for image generation
- Whisper for speech-to-text
- Embeddings for semantic search

### Azure OpenAI Service
- Enterprise-grade OpenAI models
- Private network access
- Compliance and governance
- Regional deployment

### Azure Cognitive Services
- Vision API
- Speech Services
- Language Understanding (LUIS)
- Content Moderator

### Other AI Platforms
- Anthropic Claude
- Google Vertex AI
- Hugging Face models
- Local LLMs (Ollama, LM Studio)

## Getting Started

### API Key Setup

```bash
# Set environment variables
export OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

### Basic Integration

```python
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain automation briefly."}
    ]
)

print(response.choices[0].message.content)
```

## Common Use Cases

### 1. Code Review

```python
def review_code(code: str) -> dict:
    """AI-powered code review"""
    
    prompt = f"""
    Review this code for:
    - Bugs and errors
    - Security vulnerabilities
    - Performance issues
    - Best practices
    
    Code:
    ```
    {code}
    ```
    
    Provide specific, actionable feedback.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return {
        "review": response.choices[0].message.content,
        "tokens_used": response.usage.total_tokens
    }
```

### 2. Content Generation

```python
def generate_content(topic: str, style: str = "professional") -> str:
    """Generate content on a topic"""
    
    prompt = f"""
    Write a {style} article about: {topic}
    
    Requirements:
    - 500-700 words
    - Clear structure with intro, body, conclusion
    - Engaging and informative
    - Include relevant examples
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return response.choices[0].message.content
```

### 3. Sentiment Analysis

```python
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment and extract insights"""
    
    prompt = f"""
    Analyze this text for:
    - Overall sentiment (positive/negative/neutral)
    - Key themes
    - Action items (if any)
    - Urgency level (low/medium/high)
    
    Text: {text}
    
    Provide structured JSON output.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis expert. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    
    return json.loads(response.choices[0].message.content)
```

### 4. Data Extraction

```python
def extract_structured_data(unstructured_text: str) -> dict:
    """Extract structured data from text"""
    
    prompt = f"""
    Extract the following information from the text:
    - Names (people, companies)
    - Dates and times
    - Locations
    - Email addresses
    - Phone numbers
    - Key facts
    
    Text: {unstructured_text}
    
    Return as JSON.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a data extraction specialist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    
    return json.loads(response.choices[0].message.content)
```

## Advanced Patterns

### Function Calling

```python
functions = [
    {
        "name": "send_email",
        "description": "Send an email to a recipient",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email"},
                "subject": {"type": "string", "description": "Email subject"},
                "body": {"type": "string", "description": "Email body"}
            },
            "required": ["to", "subject", "body"]
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Send an email to john@example.com about the meeting tomorrow"}
    ],
    functions=functions,
    function_call="auto"
)

# Handle function call
if response.choices[0].message.get("function_call"):
    function_name = response.choices[0].message["function_call"]["name"]
    function_args = json.loads(response.choices[0].message["function_call"]["arguments"])
    # Execute the function
```

### Embeddings and Semantic Search

```python
from openai.embeddings_utils import get_embedding, cosine_similarity

def semantic_search(query: str, documents: list) -> list:
    """Find most relevant documents using embeddings"""
    
    # Get query embedding
    query_embedding = get_embedding(query, engine="text-embedding-ada-002")
    
    # Get document embeddings
    doc_embeddings = [
        get_embedding(doc, engine="text-embedding-ada-002")
        for doc in documents
    ]
    
    # Calculate similarities
    similarities = [
        cosine_similarity(query_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]
    
    # Sort by similarity
    results = sorted(
        zip(documents, similarities),
        key=lambda x: x[1],
        reverse=True
    )
    
    return results[:5]  # Top 5 results
```

### Streaming Responses

```python
def stream_response(prompt: str):
    """Stream AI response in real-time"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.get("content"):
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
```

## Best Practices

### 1. Prompt Engineering

**Good Prompt:**
```python
prompt = """
You are a Python expert. Review this code for security issues.
Focus on: SQL injection, XSS, authentication, data validation.
Provide specific line numbers and fixes.

Code:
{code}
"""
```

**Bad Prompt:**
```python
prompt = f"Check this code: {code}"
```

### 2. Error Handling

```python
from openai.error import RateLimitError, APIError
import time

def call_ai_with_retry(func, max_retries=3):
    """Retry AI calls with exponential backoff"""
    
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            time.sleep(wait_time)
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    
    return None
```

### 3. Cost Management

```python
class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.cost_per_1k_tokens = 0.002  # GPT-3.5
    
    def track_usage(self, response):
        tokens = response.usage.total_tokens
        self.total_tokens += tokens
        cost = (tokens / 1000) * self.cost_per_1k_tokens
        return cost
    
    def get_total_cost(self):
        return (self.total_tokens / 1000) * self.cost_per_1k_tokens

tracker = CostTracker()
```

### 4. Response Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_ai_call(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Cache AI responses to reduce costs"""
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

## Testing AI Integrations

### Unit Testing

```python
import unittest
from unittest.mock import patch

class TestAIIntegration(unittest.TestCase):
    @patch('openai.ChatCompletion.create')
    def test_code_review(self, mock_create):
        # Mock AI response
        mock_create.return_value = {
            "choices": [{
                "message": {"content": "Code looks good"}
            }]
        }
        
        result = review_code("def hello(): return 'world'")
        self.assertIn("Code looks good", result["review"])
```

### Integration Testing

```python
def test_ai_pipeline():
    """Test complete AI workflow"""
    
    # Input
    input_text = "Sample customer feedback"
    
    # Process through AI pipeline
    sentiment = analyze_sentiment(input_text)
    summary = generate_summary(input_text)
    actions = extract_action_items(input_text)
    
    # Verify outputs
    assert sentiment["overall"] in ["positive", "negative", "neutral"]
    assert len(summary) > 0
    assert isinstance(actions, list)
```

## Security Considerations

### 1. API Key Protection

```python
# ❌ Bad - Never hardcode keys
api_key = "sk-abc123..."

# ✅ Good - Use environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")
```

### 2. Input Validation

```python
def validate_input(text: str) -> bool:
    """Validate user input before sending to AI"""
    
    # Check length
    if len(text) > 10000:
        return False
    
    # Check for malicious content
    dangerous_patterns = ["<script>", "DROP TABLE", "'; DELETE"]
    if any(pattern in text.lower() for pattern in dangerous_patterns):
        return False
    
    return True
```

### 3. Output Sanitization

```python
def sanitize_ai_output(text: str) -> str:
    """Clean AI output before displaying"""
    
    # Remove potential code injection
    text = text.replace("<script>", "")
    text = text.replace("</script>", "")
    
    # Escape HTML
    import html
    text = html.escape(text)
    
    return text
```

### 4. Content Filtering

```python
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient

def moderate_content(text: str) -> dict:
    """Check content for inappropriate material"""
    
    client = ContentModeratorClient(endpoint, credentials)
    
    result = client.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=text
    )
    
    return {
        "safe": result.classification.reviewed,
        "categories": result.classification.category1.score
    }
```

## Monitoring and Observability

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_ai_call(prompt: str):
    """AI call with logging"""
    
    logger.info(f"Making AI call with prompt: {prompt[:100]}...")
    
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    duration = time.time() - start_time
    
    logger.info(f"AI call completed in {duration:.2f}s")
    logger.info(f"Tokens used: {response.usage.total_tokens}")
    
    return response
```

### Metrics

```python
from prometheus_client import Counter, Histogram

ai_requests = Counter('ai_requests_total', 'Total AI API requests')
ai_latency = Histogram('ai_request_duration_seconds', 'AI request duration')
ai_tokens = Counter('ai_tokens_total', 'Total tokens used')

@ai_latency.time()
def monitored_ai_call(prompt: str):
    ai_requests.inc()
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    ai_tokens.inc(response.usage.total_tokens)
    
    return response
```

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/cognitive-services/openai/)
- [LangChain Documentation](https://python.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [AI Safety Best Practices](https://openai.com/safety)

## Example Projects

See `/ai-examples` directory for complete implementations:

1. **Code Review Assistant** - Automated code analysis
2. **Content Generator** - Blog and social media posts
3. **Meeting Summarizer** - Extract insights from transcripts
4. **Support Agent** - AI-powered customer service
