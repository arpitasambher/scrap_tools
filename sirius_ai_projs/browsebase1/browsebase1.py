import os
from dotenv import load_dotenv
from crewai_tools import BrowserbaseLoadTool

# Load the environment variables from .env file
load_dotenv()

# Optional: print to verify (delete later)
print("API Key:", os.getenv("BROWSERBASE_API_KEY"))
print("Project ID:", os.getenv("BROWSERBASE_PROJECT_ID"))

# Use the tool
tool = BrowserbaseLoadTool(
    api_key=os.getenv("BROWSERBASE_API_KEY"),
    project_id=os.getenv("BROWSERBASE_PROJECT_ID")
)

result = tool.run(website_url="https://example.com")

print(result)
