# MCP WebScraper

A minimal yet powerful AI-powered web scraping agent built with FastMCP, Playwright, and OpenAI’s LLMs. This scraper is designed to extract structured data—such as real estate listings—from dynamic websites and return clean, validated JSON using a custom Pydantic schema.

## What It Does

This tool launches a headless browser, navigates to a real estate listings site, extracts the relevant HTML section, and delegates the parsing task to a Language Model (LLM). The output is structured JSON, ready to be consumed by downstream tools like Google Sheets or your own AI agent.

The scraper is registered as an MCP Tool and can be called programmatically from platforms like n8n.

---

## Tech Stack

- FastMCP – Lightweight server to register AI-powered tools
- Playwright – Controls the browser in headless mode
- OpenAI GPT-4o-mini – Parses messy HTML into structured JSON
- Pydantic – Data validation and modeling
- dotenv – Secrets management via .env
- nest_asyncio – Async patching for mixed environments

---

## Setup Instructions

If you’ve cloned this repository, follow these steps to run the project locally.

### Prerequisites

Make sure you have Python 3.10+ and `uv` installed. If not, you can install `uv` with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. Clone the repository (if you haven’t already):

```bash
git clone https://github.com/your-username/mcp-webscraper.git
cd mcp-webscraper
```

2. Create and activate a virtual environment using `uv`:

```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies from the `pyproject.toml`:

```bash
uv pip install .
```

4. Create a `.env` file at the root of the project and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-key
```

5. Run the application:

```bash
python main.py
```

This will start the MCP server and make the tool available for integration.