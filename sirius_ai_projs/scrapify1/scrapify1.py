from dotenv import load_dotenv
import os
from crewai_tools import ScrapflyScrapeWebsiteTool

load_dotenv()
api_key = os.getenv("SCRAPFLY_API_KEY")

tool = ScrapflyScrapeWebsiteTool(api_key=api_key)

result = tool.run(
    url="https://web-scraping.dev/products",
    scrape_format="markdown",  # or "raw", "text"
    scrape_config={
        "render_js": True,
        "auto_scroll": True
    }
)

with open("scrapfly_output.md", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Content saved to scrapfly_output.md")
