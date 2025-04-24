from mcp.server.fastmcp import FastMCP
from src.scraper_tool import webscraper, WebScraperAgent
from src.format_output import ListingResponse

# Initialize MCP server
mcp = FastMCP("WebScraper")

# Define web scraper tool
@mcp.tool()
async def scrape_listings(query: str, instructions: str) -> ListingResponse:
    """
    Scrapes real estate listings based on a city query and user instructions.

    Args:
        query: City or location to search listings for (e.g., "Bogota").
        instructions: LLM instructions for how to extract data from the HTML.

    Returns:
        A structured ListingResponse with the extracted results.
    """
    print(f"📥 Received scrape request for: {query}")
    target_url = f"https://www.fincaraiz.com.co/arriendo/apartamentos/{query}"

    scraper_agent_instance = WebScraperAgent()
    result = None

    try:
        result = await webscraper(
            scraper_agent=scraper_agent_instance,
            target_url=target_url,
            instructions=instructions
        )
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return ListingResponse(listings=[])
    finally:
        print("🧹 Closing browser session...")
        await scraper_agent_instance.close()

    return result if isinstance(result, ListingResponse) else ListingResponse(listings=[])

# Run the MCP server
if __name__ == "__main__":
    print("🚀 Starting MCP server for Listing Scraper...")
    mcp.run(transport='sse')