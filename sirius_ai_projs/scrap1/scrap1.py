from crewai_tools import ScrapeWebsiteTool

# Initialize the tool with a specific website URL
tool = ScrapeWebsiteTool(website_url='https://medium.com/@kabilankb2003/object-detection-in-ros2-with-pytorchs-faster-bb54a65e47e0')

# Run the tool to get the website content
result = tool.run()

# Save result to file
with open("scraped_output.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Scraped content saved to scraped_output.txt")
