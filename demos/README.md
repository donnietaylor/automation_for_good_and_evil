# Demo Examples

This directory contains ready-to-run demonstration code for the "Automation for Good and Evil" presentation.

## Available Demos

### 1. Good Examples

#### Auto-Code-Review Bot
- **Location**: `./good/auto-code-review/`
- **Description**: An AI-powered code review bot that provides helpful feedback
- **Tech**: Azure Functions, OpenAI API
- **Run Time**: 5 minutes

#### Smart Email Assistant
- **Location**: `./good/email-assistant/`
- **Description**: Intelligently categorizes and responds to emails
- **Tech**: Azure Logic Apps, AI text classification
- **Run Time**: 3 minutes

#### Intelligent Meeting Scheduler
- **Location**: `./good/meeting-scheduler/`
- **Description**: Finds optimal meeting times respecting time zones and preferences
- **Tech**: Microsoft Graph API, Azure Functions
- **Run Time**: 4 minutes

### 2. Evil Examples

#### Overly Enthusiastic Bot
- **Location**: `./evil/enthusiastic-bot/`
- **Description**: Responds to EVERYTHING with excessive enthusiasm
- **Tech**: n8n, OpenAI API
- **Run Time**: 3 minutes

#### Meeting Conflict Generator
- **Location**: `./evil/meeting-chaos/`
- **Description**: Intentionally creates scheduling conflicts (for demo purposes!)
- **Tech**: Azure Logic Apps, Calendar APIs
- **Run Time**: 5 minutes

#### Code Format Wars
- **Location**: `./evil/format-wars/`
- **Description**: Randomly switches between tabs and spaces
- **Tech**: Python, Git hooks
- **Run Time**: 2 minutes

## Running the Demos

Each demo folder contains:
- `README.md` - Specific setup instructions
- `setup.sh` or `setup.ps1` - Automated setup script
- Source code files
- `.env.example` - Required environment variables

### General Setup

1. Copy `.env.example` to `.env` in the demo directory
2. Fill in your API keys and credentials
3. Run the setup script
4. Follow demo-specific instructions

### Prerequisites

See main README for general prerequisites. Demo-specific requirements are listed in each demo's README.

## Demo Guidelines

- Always test demos before the presentation
- Have backup plans for API failures
- Keep sensitive credentials in `.env` files (never commit these!)
- Reset demo state between runs

## Adding New Demos

To add a new demo:
1. Create a new folder under `good/` or `evil/`
2. Add a descriptive README.md
3. Include a `.env.example` with required variables
4. Add a setup script
5. Test thoroughly!
