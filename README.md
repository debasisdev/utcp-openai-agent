# UTCP OpenAI Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?logo=python)](https://www.python.org/) 

A Python-based AI assistant that leverages OpenAI's GPT models with UTCP (Universal Tool Calling Protocol) integration. This agent provides a command-line interface for interacting with various tools through natural language.

## Features

- 🤖 Interactive AI assistant powered by GPT-4 family models
- 🛠️ UTCP (Universal Tool Calling Protocol) integration for tool access
- 🔧 Extensible tool system — add or map UTCP tools into the agent
- 🌍 Environment variable support through dotenv
- 💬 Simple command-line interface for quick interactions

## Prerequisites

- Python 3.8+
- OpenAI API access (API key set in `.env`)
- UTCP service configuration (see `utcp-config.json`)

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/debasisdev/utcp-openai-agent.git
cd utcp-openai-agent
```

2. Install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Copy the example environment file and update values:

```bash
cp example.env .env
# Edit .env and add OPENAI_API_KEY, COINGECKO_API_KEY, etc.
```

4. Run the agent:

```bash
python agent.py
```

Type natural language prompts at the prompt and `exit` to quit.

## Configuration

Key configuration files:

- `utcp-config.json`: UTCP variables, variable loaders, and manual call templates
- `utcp.json`: Service catalog and tool definitions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[debasisdev](https://github.com/debasisdev)
