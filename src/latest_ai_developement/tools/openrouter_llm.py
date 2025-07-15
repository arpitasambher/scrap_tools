import os
import requests
from langchain.llms.base import LLM

class OpenRouterLLM(LLM):
    """Custom LLM wrapper for OpenRouter API."""
    api_key: str = os.getenv("OPENROUTER_API_KEY")

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def _call(self, prompt: str, stop=None) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenRouter API Error: {response.status_code}, {response.text}")
