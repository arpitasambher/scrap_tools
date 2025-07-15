from crewai_tools import BaseTool
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class OpenRouterLLMTool(BaseTool):
    name: str = "OpenRouter LLM Tool"
    description: str = "Generates text using the OpenRouter API for data permutations or summarization."

    def _run(self, prompt: str) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",
            "X-Title": "AMLResearchAgent"
        }
        body = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            res = requests.post(url, headers=headers, data=json.dumps(body))
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
            return f"Error: {res.status_code} - {res.text}"
        except Exception as e:
            return f"Exception: {str(e)}"
