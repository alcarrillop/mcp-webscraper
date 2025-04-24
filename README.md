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

1. Install uv package manager:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create project and install dependencies:

```
uv init mcp-webscraper
cd mcp-webscraper
uv venv
source .venv/bin/activate
uv add "mcp[cli]" playwright nest_asyncio pydantic openai
```

3. Create project structure:

```
mkdir src
touch src/scraper_tool.py src/format_output.py .env
```

4. Set your .env file:

```
OPENAI_API_KEY=your-openai-key
```

---

## Example Usage (via n8n)

You can integrate this scraper as a tool in an n8n agent with the following prompt:

```
You are an expert web scraping agent. Your task is to extract the following:
- Title, location, price, bedrooms, bathrooms, area
- Realtor's name, image URL, full listing link
Return ONLY valid JSON conforming to the ListingResponse schema.
```

---

## Run Locally

```
python main.py
```

Then hit the endpoint with a tool call (query + instructions). The server will handle browser orchestration, LLM interaction, and return JSON with:

```
{
  "title": "Apartment in Bucaramanga",
  "price": "$1,250,000",
  ...
}
```

---

## Project Structure

```
mcp-webscraper/
├── src/
│   ├── scraper_tool.py     # Web scraping and LLM logic
│   └── format_output.py    # Pydantic models
├── .env                    # API key (not committed)
├── main.py                 # MCP tool server
├── README.md
```

---

## Future Ideas

- Add support for multiple listing websites
- Dynamic selector detection using GPT-4
- Automatic sheet export integration
- Memory persistence across sessions via MCP

---

## About the Creator

This project is part of my journey exploring how agents can use tools in autonomous workflows. I enjoy building things that combine data, language models, and real-world automation.

If this resonates with you, let’s connect.