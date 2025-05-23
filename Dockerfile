# Generated by https://smithery.ai. See: https://smithery.ai/docs/build/project-config
FROM python:3.10-slim

# Install Ledger CLI and OS dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends ledger \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock main.py /app/

# Install project and CLI
RUN pip install --no-cache-dir . "mcp[cli]>=1.4.1"

# Default command (overridden by MCP host)
CMD ["mcp", "run", "main.py"]
