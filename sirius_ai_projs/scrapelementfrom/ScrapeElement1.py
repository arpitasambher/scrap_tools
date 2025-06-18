from crewai_tools import ScrapeElementFromWebsiteTool

# Initialize tool with URL and CSS selector
tool = ScrapeElementFromWebsiteTool(
    website_url='https://quotes.toscrape.com',
    css_element='.quote'
)

# Run the scraper
result = tool.run()

# Save to file
with open("scraped_quotes.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Scraped content saved to scraped_quotes.txt")
