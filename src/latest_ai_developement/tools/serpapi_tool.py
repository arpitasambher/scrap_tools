from crewai_tools import BaseTool
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class SerpApiTool(BaseTool):
    name: str = "SerpAPI Search Tool"
    description: str = "Fetches search results from Google using SerpAPI."

    def _run(self, query: str) -> str:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 3
        }
        try:
            res = requests.get(url, params=params)
            if res.status_code == 200:
                data = res.json()
                return str(data.get("organic_results", []))
            return f"Error: {res.status_code} - {res.text}"
        except Exception as e:
            return f"Exception: {str(e)}"
