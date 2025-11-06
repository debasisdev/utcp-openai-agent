# UTCP OpenAI Agent

A Python-based AI assistant that leverages OpenAI's GPT models with UTCP (Universal Tool Calling Protocol) integration. This agent provides a command-line interface for interacting with various tools through natural language.

## Features

- 🤖 Interactive AI assistant powered by GPT-4
- 🛠️ UTCP (Universal Tool Calling Protocol) integration
- 🔧 Extensible tool system
- 🌍 Environment variable support through dotenv
- 💬 User-friendly command-line interface

## Prerequisites

- Python 3.x
- OpenAI API access
- UTCP service configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/debasisdev/utcp-openai-agent.git
cd utcp-openai-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on the example:
```bash
cp example.env .env
```

4. Configure your environment variables in the `.env` file:
- Add your OpenAI API key
- Add your COINGECKO API key (if needed)
- Configure any other required credentials

## Configuration

The project uses two main configuration files:

- `utcp-config.json`: Configures UTCP variables and service templates
- `utcp.json`: Contains service catalog definitions

## Usage

1. Start the agent:
```bash
python agent.py
```

2. Interact with the agent through the command-line interface:
- Type your requests in natural language
- Type 'exit' to quit the application

## Project Structure

```
├── agent.py              # Main application entry point
├── openai_bridge.py      # OpenAI and UTCP integration
├── requirements.txt      # Project dependencies
├── utcp-config.json     # UTCP configuration
├── utcp.json            # Service catalog definition
└── example.env          # Environment variables template
```

## Dependencies

- python-dotenv: Environment variable management
- openai: OpenAI API client
- openai-agents: Agent framework
- utcp: Universal Tool Calling Protocol
- utcp-text: UTCP text processing utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

[debasisdev](https://github.com/debasisdev)