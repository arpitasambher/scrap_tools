from dotenv import load_dotenv
import os
from crewai_tools.tools.firecrawl_crawl_website_tool.firecrawl_crawl_website_tool import FirecrawlCrawlWebsiteTool

load_dotenv()
api_key = os.getenv("FIRECRAWL_API_KEY")

tool = FirecrawlCrawlWebsiteTool(
    url="https://www.flipkart.com/",
    api_key=api_key
)

result = tool.run(url="https://www.flipkart.com/")

# Get the first document
doc = result.data[0]  # FirecrawlDocument object

# Print the content
print(doc.markdown)

# Optional: save to file
with open("flip.md", "w", encoding="utf-8") as f:
    f.write(doc.markdown)

