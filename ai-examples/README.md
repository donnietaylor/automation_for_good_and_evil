# AI Examples

This directory contains AI-powered automation examples demonstrating both helpful and humorous use cases.

## AI Technologies Used

- **OpenAI GPT Models** - Text generation and analysis
- **Azure OpenAI Service** - Enterprise-grade AI
- **Azure Cognitive Services** - Vision, speech, language understanding
- **LangChain** - LLM application framework
- **Custom Fine-tuned Models** - Specialized use cases

## Examples Overview

### Good AI Automations 😇

#### 1. Code Review Assistant
**Location**: `./good/code-review-assistant/`

Automatically reviews code and provides constructive feedback.

**Features:**
- Analyzes code quality
- Suggests improvements
- Checks for common bugs
- Reviews security issues

**Tech Stack:** Python, OpenAI API, GitHub API

#### 2. Documentation Generator
**Location**: `./good/doc-generator/`

Creates comprehensive documentation from code.

**Features:**
- Generates API documentation
- Creates usage examples
- Writes README sections
- Produces inline comments

**Tech Stack:** Python, LangChain, Azure OpenAI

#### 3. Smart Meeting Summarizer
**Location**: `./good/meeting-summarizer/`

Transcribes and summarizes meetings with action items.

**Features:**
- Speech-to-text transcription
- Key points extraction
- Action item identification
- Participant tracking

**Tech Stack:** Azure Cognitive Services, Python

### Evil AI Automations 😈

#### 1. Overly Excited Email Responder
**Location**: `./evil/excited-responder/`

Responds to emails with excessive enthusiasm and emojis.

**Features:**
- Adds random emojis 🎉🚀⭐
- USES CAPS LOCK RANDOMLY
- Includes multiple exclamation points!!!
- Asks too many questions???

**Tech Stack:** Python, OpenAI API, SMTP

#### 2. Meeting Jargon Generator
**Location**: `./evil/jargon-generator/`

Fills meetings with corporate buzzwords.

**Features:**
- Synergizes stakeholder alignment
- Leverages paradigm shifts
- Optimizes bandwidth utilization
- Circles back to touch base

**Tech Stack:** Python, OpenAI API with custom prompts

#### 3. Autocorrect Chaos
**Location**: `./evil/autocorrect-chaos/`

Autocorrects things that don't need correcting.

**Features:**
- Changes correct words to "better" words
- Adds random "improvements"
- Context-free suggestions
- Never learns from mistakes

**Tech Stack:** Python, Custom NLP model

## Setup Instructions

### General Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### API Keys Required

```env
OPENAI_API_KEY=your_openai_key
AZURE_OPENAI_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_COGNITIVE_SERVICES_KEY=your_key
```

## Running Examples

Each example directory contains:
- `README.md` - Detailed instructions
- `main.py` or `app.py` - Main application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variable template
- `tests/` - Unit tests (where applicable)

### Quick Start

```bash
cd ai-examples/good/code-review-assistant
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python main.py
```

## Safety Considerations

### Good Examples
- Rate limiting implemented
- Cost controls in place
- Privacy-preserving (no data retention)
- Error handling for API failures

### Evil Examples
- Clearly marked as demonstrations
- Limited scope to prevent actual harm
- Require explicit confirmation before running
- Easy to disable or revert

## Cost Management

AI API calls can be expensive. Tips to manage costs:

1. **Use caching** - Cache API responses when possible
2. **Set token limits** - Limit maximum tokens per request
3. **Use cheaper models** - Start with GPT-3.5 before GPT-4
4. **Monitor usage** - Check API usage regularly
5. **Set budget alerts** - Configure spending alerts

## Best Practices

### Prompt Engineering
```python
# Good: Clear, specific instructions
prompt = "Review the following Python function for bugs and security issues: {code}"

# Evil: Vague, open-ended
prompt = "Say something about this code: {code}"
```

### Error Handling
```python
try:
    response = openai.ChatCompletion.create(...)
except openai.error.RateLimitError:
    # Handle rate limiting
    pass
except openai.error.APIError:
    # Handle API errors
    pass
```

### Context Management
- Keep context windows manageable
- Summarize long conversations
- Clear context when switching topics

## Testing AI Applications

```bash
# Run tests for a specific example
cd good/code-review-assistant
pytest tests/

# Run all tests
pytest ai-examples/
```

## Common Issues

### Issue: API Key Not Found
**Solution**: Ensure `.env` file is created and contains valid keys

### Issue: Rate Limit Exceeded
**Solution**: Implement exponential backoff, use caching

### Issue: Poor Quality Responses
**Solution**: Improve prompts, use few-shot examples, adjust temperature

## Contributing New Examples

To add a new AI example:

1. Create appropriate subdirectory (`good/` or `evil/`)
2. Include `README.md` with clear description
3. Add `requirements.txt` for dependencies
4. Create `.env.example` with needed keys
5. Implement proper error handling
6. Add tests where applicable
7. Document any costs or rate limits

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [LangChain Documentation](https://python.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## Responsible AI

Remember:
- Respect user privacy
- Be transparent about AI usage
- Consider bias in AI models
- Provide human oversight
- Allow users to opt-out
- Handle data responsibly
