


import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from google import genai

# Load .env
load_dotenv(dotenv_path="/workspace/siriusAI/temp1/project-root/src/latest_ai_development/.env")

# Initialize Gemini client
client = genai.Client()

# Define output schema
class SummaryItem(BaseModel):
    url: str
    summary: str

def summarize(topic: str):
    """
    Summarize AML-related content from scraped data using Gemini (structured).
    Outputs JSON AML report.
    """
    print(f"[UTIL] Summarizing research on topic: {topic}")

    scraped_file = "output/scraped_data.json"
    if not os.path.exists(scraped_file):
        raise FileNotFoundError("❌ scraped_data.json not found. Run scraping first.")

    with open(scraped_file, "r") as f:
        scraped_results = json.load(f)

    summaries: List[SummaryItem] = []

    for idx, item in enumerate(scraped_results, start=1):
        url = item.get("url")
        content = item.get("content", "")

        if not content.strip():
            print(f"⚠️ Skipping {url}, no content found.")
            continue

        print(f"➡️ Summarizing content from URL {idx}/{len(scraped_results)}: {url}")

        prompt = f"""
You are a helpful assistant for Anti-Money Laundering (AML) investigators.

Your job is to summarize the following webpage content, focusing only on:
- Money laundering
- Financial fraud
- Suspicious financial activity

Return exactly two fields:
1. `url`: The page URL.
2. `summary`: The extracted summary related to AML. If nothing is relevant, return "No relevant AML content found."

### URL:
{url}

### Page Content:
{content[:2000]}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                "response_mime_type": "application/json",
                "response_schema": SummaryItem,
                }
            )


            summary_item: SummaryItem = response.parsed
            summaries.append(summary_item)
            print(f"✅ Summary generated for {url}")

        except Exception as e:
            print(f"❌ Error summarizing {url}: {e}")
            summaries.append(SummaryItem(url=url, summary=f"Error: {e}"))

    # Save final AML report
    aml_report = {
        "topic": topic,
        "total_urls": len(scraped_results),
        "summaries": [item.model_dump() for item in summaries]

    }

    os.makedirs("output", exist_ok=True)
    with open("output/aml_report1.json", "w") as f:
        json.dump(aml_report, f, indent=2)

    print("[UTIL] ✅ AML report saved to output/aml_report1.json")
    return aml_report





