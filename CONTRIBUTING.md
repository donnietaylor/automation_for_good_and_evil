# Contributing to Automation for Good and Evil

Thank you for your interest in contributing! This repository is primarily for demonstration purposes, but we welcome contributions that add value to the presentation materials.

## How to Contribute

### 1. Types of Contributions Welcome

- **New Automation Examples**: Both "good" and "evil" (humorous) examples
- **Documentation Improvements**: Clarifications, corrections, additional guides
- **Bug Fixes**: Fixing issues in existing examples
- **Presentation Materials**: New slides, graphics, or speaker notes
- **Demo Enhancements**: Improvements to live demo code

### 2. Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/automation_for_good_and_evil.git
   cd automation_for_good_and_evil
   ```

3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 3. Contribution Guidelines

#### Code Examples

- **Follow existing structure**: Place examples in appropriate folders (`good/` or `evil/`)
- **Include README**: Each example should have clear documentation
- **Add `.env.example`**: Include template for required environment variables
- **Test thoroughly**: Ensure examples work before submitting
- **Keep it simple**: Examples should be easy to understand and demonstrate a clear point

#### Documentation

- **Use clear language**: Write for a general technical audience
- **Include examples**: Show, don't just tell
- **Check formatting**: Ensure Markdown renders correctly
- **Update TOC**: Update relevant table of contents if needed

#### "Evil" Examples

Remember, "evil" examples should be:
- **Humorous** and obviously problematic
- **Safe** to run in demo environments
- **Educational** - show what not to do
- **Reversible** - easy to undo any changes
- **Ethical** - never actually harmful

### 4. Code Standards

#### Python

```python
# Use type hints
def process_data(input: str) -> dict:
    """
    Process input data.
    
    Args:
        input: Input string to process
        
    Returns:
        Dictionary with processed results
    """
    pass

# Follow PEP 8
# Use meaningful variable names
# Add docstrings to functions
```

#### JavaScript/TypeScript

```typescript
// Use TypeScript where possible
interface Config {
  apiKey: string;
  endpoint: string;
}

// Document functions
/**
 * Processes webhook data
 * @param data - Incoming webhook payload
 * @returns Processed result
 */
function processWebhook(data: any): Result {
  // Implementation
}

// Use async/await
async function fetchData(): Promise<Data> {
  const response = await fetch(url);
  return await response.json();
}
```

### 5. Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add email automation example with OpenAI integration"
- "Fix typo in Azure Functions documentation"
- "Update README with new workflow examples"

Bad:
- "Update"
- "Fix stuff"
- "Changes"
```

Format:
```
<type>: <short description>

<optional longer description>

<optional references>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

### 6. Pull Request Process

1. **Update documentation**: Reflect any changes in relevant docs
2. **Test your changes**: Ensure everything works
3. **Create pull request**: 
   - Use a clear title
   - Describe what you changed and why
   - Reference any related issues
   - Include screenshots for UI changes

4. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] New example
   - [ ] Bug fix
   - [ ] Documentation update
   - [ ] Other (describe)
   
   ## Testing
   How you tested the changes
   
   ## Screenshots (if applicable)
   Add screenshots here
   
   ## Additional Notes
   Any other relevant information
   ```

### 7. Review Process

- Maintainers will review your PR
- Be responsive to feedback
- Make requested changes
- Once approved, your PR will be merged

### 8. Setting Up Development Environment

#### For Azure Examples

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
```

#### For n8n Examples

```bash
# Using Docker
docker run -it --rm -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

#### For MCP Servers

```bash
# Install Node.js 18+
nvm install 18
nvm use 18

# Install dependencies
npm install
```

#### For AI Examples

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env with your keys
```

### 9. Adding New Examples

#### Good Example Template

```
/demos/good/your-example/
├── README.md           # Clear description and setup
├── .env.example        # Environment variables template
├── setup.sh           # Automated setup script
├── main.py            # Main implementation
├── requirements.txt   # Dependencies
└── tests/             # Tests (optional but encouraged)
```

#### Evil Example Template

```
/demos/evil/your-example/
├── README.md           # Description, warning about "evil" nature
├── .env.example        # Environment variables template
├── setup.sh           # Automated setup script
├── main.py            # Implementation with safety limits
├── requirements.txt   # Dependencies
└── reset.sh           # Script to undo changes
```

### 10. Questions?

- Open an issue for discussion
- Tag with `question` label
- Be patient - this is a side project!

### 11. Code of Conduct

Be respectful and professional:
- Be welcoming to newcomers
- Be patient with questions
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### 12. Recognition

Contributors will be recognized in:
- README contributors section
- Release notes for significant contributions
- Presentation acknowledgments (if appropriate)

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

*Remember: We're here to learn, teach, and have fun with automation!*
