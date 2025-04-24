import os
import nest_asyncio
from dotenv import load_dotenv, find_dotenv
from playwright.async_api import async_playwright
from openai import OpenAI
from bs4 import BeautifulSoup
from src.format_output import ListingResponse

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Initialize OpenAI client using API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Patch asyncio to allow nested event loops (used by some async environments)
nest_asyncio.apply()


class WebScraperAgent:
    """Agent to control a headless Chromium browser using Playwright."""
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-accelerated-2d-canvas",
                "--disable-gpu",
                "--no-zygote",
                "--disable-audio-output",
                "--disable-software-rasterizer",
                "--disable-webgl",
                "--disable-web-security",
                "--disable-features=LazyFrameLoading",
                "--disable-features=IsolateOrigins",
                "--disable-background-networking"
            ]
        )
        self.page = await self.browser.new_page()

    async def scrape_content(self, url: str) -> str:
        """Loads the target page and returns its HTML content."""
        if not self.page or self.page.is_closed():
            await self.init_browser()
        await self.page.goto(url, wait_until="load")
        try:
            await self.page.wait_for_selector("div.title", timeout=7000)
        except:
            await self.page.wait_for_timeout(3000)
        return await self.page.content()

    async def close(self):
        """Closes the browser and cleans up resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None
        self.browser = None
        self.page = None


def extract_listings_html(html: str) -> str:
    """Extracts only the listings section from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    section = soup.select_one("section.listingsWrapper")
    return str(section) if section else html


async def process_with_llm(html: str, instructions: str, response_model, truncate: bool = False):
    """Sends cleaned HTML and instructions to the LLM for JSON parsing."""
    html_to_send = html[:100000] if truncate else html

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert web scraping agent. Your task is to extract specific information
                from the provided HTML and return it as JSON. Follow these instructions carefully: {instructions}

                Output ONLY valid JSON that matches the specified model structure. Do not include markdown or extra text.
                """
            },
            {
                "role": "user",
                "content": html_to_send
            }
        ],
        temperature=0.1,
        response_format=response_model,
    )
    return completion.choices[0].message.parsed


async def webscraper(scraper_agent: WebScraperAgent, target_url: str, instructions: str):
    """Orchestrates the scraping and LLM processing pipeline."""
    try:
        if not scraper_agent.playwright:
            await scraper_agent.init_browser()

        print(f"🔍 Extracting content from {target_url}")
        html = await scraper_agent.scrape_content(target_url)

        print("🧹 Filtering relevant content...")
        filtered_html = extract_listings_html(html)

        print("🧠 Sending content to LLM for processing...")
        result: ListingResponse = await process_with_llm(
            html=filtered_html,
            instructions=instructions,
            response_model=ListingResponse,
            truncate=True
        )

        print("✅ Structured data received.")
        return result

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return None