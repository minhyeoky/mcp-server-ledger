[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/minhyeoky-mcp-server-ledger-badge.png)](https://mseep.ai/app/minhyeoky-mcp-server-ledger)

# mcp-server-ledger: A Ledger CLI MCP Server

[![smithery badge](https://smithery.ai/badge/@minhyeoky/mcp-ledger)](https://smithery.ai/server/@minhyeoky/mcp-ledger)

## Overview

A Model Context Protocol server for interacting with [Ledger CLI](https://www.ledger-cli.org/), a powerful, double-entry accounting system accessible from the command line. This server allows Large Language Models to query and analyze your financial data through the Ledger CLI tool.

This MCP server exposes Ledger CLI's functionality through a standardized interface, making it easy for AI assistants to help you with financial reporting, budget analysis, and accounting tasks.

## Features

The server provides the following tools that map to Ledger CLI commands:

1. `ledger_balance`
   - Shows account balances with powerful filtering options
   - Inputs: query pattern, date ranges, display options
   - Returns: Formatted balance report

2. `ledger_register`
   - Shows transaction register with detailed history
   - Inputs: query pattern, date ranges, sorting options
   - Returns: Formatted register report

3. `ledger_accounts`
   - Lists all accounts in the ledger file
   - Input: optional query pattern
   - Returns: List of matching accounts

4. `ledger_payees`
   - Lists all payees from transactions
   - Input: optional query pattern
   - Returns: List of matching payees

5. `ledger_commodities`
   - Lists all commodities (currencies) used
   - Input: optional query pattern
   - Returns: List of matching commodities

6. `ledger_print`
   - Prints transactions in ledger format
   - Inputs: query pattern, date ranges
   - Returns: Formatted ledger entries

7. `ledger_stats`
   - Shows statistics about the ledger file
   - Input: optional query pattern
   - Returns: Statistical summary of the ledger

8. `ledger_budget`
   - Shows budget analysis
   - Inputs: query pattern, date ranges, reporting period
   - Returns: Budget report

9. `ledger_raw_command`
   - Runs a raw Ledger CLI command
   - Input: command arguments as a list of strings
   - Returns: Command output as text

## Prerequisites

- [Ledger CLI](https://www.ledger-cli.org/) must be installed and available in your PATH
- A valid Ledger file with your financial data

## Installation

### Using Docker (recommended)

You can also use the Docker image from the minhyeoky/mcp-ledger repository:

```bash
docker pull minhyeoky/mcp-ledger
```

Add this to your `claude_desktop_config.json`:

```json
"mcp-ledger": {
  "command": "docker",
  "args": [
    "run",
    "-v",
    "/path/to/your/ledger/file.ledger:/main.ledger",
    "-e",
    "LEDGER_FILE=/main.ledger",
    "-i",
    "--rm",
    "minhyeoky/mcp-ledger"
  ]
}
```

Replace `/path/to/your/ledger/file.ledger` with the actual path to your ledger file.

### Installing via Smithery

To install Ledger CLI MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@minhyeoky/mcp-ledger):

```bash
npx -y @smithery/cli install @minhyeoky/mcp-ledger --client claude
```

### Using uv

The easiest way to install and run this server is with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```
## Configuration

The server requires a path to your Ledger file. This can be provided through:

- The `LEDGER_FILE` environment variable
- Command-line arguments when starting the server

### Using with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "ledger": {
    "command": "uv",
    "args": [
      "run",
      "--env-file",
      "/path/to/your/.env",  // Optional: to set LEDGER_FILE
      "--with",
      "mcp[cli]",
      "mcp",
      "run",
      "<repo_path>/main.py"  // Path to the main.py file in this repository
    ]
  }

}
```

## Usage Examples

Once configured, you can ask your AI assistant questions about your financial data:

- "Show me my expenses for the last month"
- "What's my current balance in all accounts?"
- "List all transactions with Amazon"
- "How much did I spend on groceries in 2023?"
- "Show me my budget performance for Q1"

The AI will use the appropriate Ledger CLI commands through the server to get the information.

## Debugging

For more detailed local testing:

```bash
mcp dev main.py
```

## Development

This server is built using the [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk). For more information about MCP and how to develop MCP servers, see the [official documentation](https://modelcontextprotocol.io).

To contribute to this project:

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Test using the MCP inspector or by integrating with Claude Desktop

## Security Considerations

This server runs Ledger CLI commands on your financial data. While it includes basic validation to prevent command injection, you should:

- Only use with trusted clients
- Be careful about which file paths you expose
- Review all commands before execution

## License

This MCP server is licensed under the MIT License. Feel free to use, modify, and distribute it according to the license terms.
