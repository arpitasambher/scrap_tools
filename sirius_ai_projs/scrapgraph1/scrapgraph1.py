from crewai_tools import ScrapegraphScrapeTool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")

# Initialize the tool with website and prompt
tool = ScrapegraphScrapeTool(
    api_key=api_key,
    website_url="https://books.toscrape.com",
    user_prompt="Extract the book titles and their prices"
)

# Run the scraping
result = tool.run()

# Save the result to a text file
with open("books_output.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Scraped content saved to books_output.txt")
