from crewai_tools import BaseTool
import requests

class ScraperTool(BaseTool):
    name: str = "Web Scraper Tool"
    description: str = "Scrapes raw text from a given URL."

    def _run(self, url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                text = res.text.replace("\\n", " ").strip()
                return text[:2000]
            return f"Error: {res.status_code}"
        except Exception as e:
            return f"Exception: {str(e)}"
