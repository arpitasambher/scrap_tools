# def summarize(topic):
#     """Mock summarizer logic."""
#     print(f"[UTIL] Summarizing research on topic: {topic}")
#     return f"Summary report for {topic}: Research data analyzed and compiled."


import os
import json
import requests
from dotenv import load_dotenv

# Load .env (important for Jupyter)
load_dotenv(dotenv_path="/workspace/siriusAI/temp1/project-root/src/latest_ai_development/.env")

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY not loaded. Check your .env file path.")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def summarize(topic):
    """
    Summarize AML-related content from scraped data using OpenRouter API and save AML report.
    Reads scraped_data.json, processes summaries, and outputs aml_report.json.
    """

    print(f"[UTIL] Summarizing research on topic: {topic}")

    # Check if scraped data exists
    scraped_file = "output/scraped_data.json"
    if not os.path.exists(scraped_file):
        raise FileNotFoundError("❌ scraped_data.json not found. Run scraping first.")

    with open(scraped_file, "r") as f:
        scraped_results = json.load(f)

    summaries = []
    for idx, item in enumerate(scraped_results, start=1):
        url = item.get("url")
        content = item.get("content", "")

        if not content.strip():
            print(f"⚠️ Skipping {url}, no content found.")
            continue

        print(f"➡️ Summarizing content from URL {idx}/{len(scraped_results)}: {url}")
        prompt = f"""You are a helpful assistant. Summarize the following article focusing ONLY on:
- Money laundering
- Financial fraud
- Suspicious financial activities

If nothing relevant is found, respond: "No relevant AML content found."

### URL:
{url}

### Extracted Text:
{content[:2000]}"""  # Increased to 2000 chars for better context

        try:
            # Call OpenRouter API
            response = requests.post(
                API_URL,
                headers=HEADERS,
                json={
                    "model": "meta-llama/llama-3-8b-instruct",  # You can change to another model
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 800
                },
                timeout=180
            )

            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}: {response.text}")

            output = response.json().get("choices", [])[0].get("message", {}).get("content", "").strip()
            summaries.append({
                "url": url,
                "summary": output if output else "⚠️ No summary generated"
            })
            print(f"✅ Summary generated for {url}")

        except Exception as e:
            print(f"❌ Error summarizing {url}: {e}")
            summaries.append({
                "url": url,
                "summary": f"Error: {e}"
            })

    # Save summaries to AML report file
    aml_report = {
        "topic": topic,
        "total_urls": len(scraped_results),
        "summaries": summaries
    }

    os.makedirs("output", exist_ok=True)
    with open("output/aml_report.json", "w") as f:
        json.dump(aml_report, f, indent=2)

    print(f"[UTIL] ✅ AML report saved to output/aml_report.json")
    return aml_report


# import os
# import json
# import requests
# from dotenv import load_dotenv

# # Load .env (important for Jupyter)
# load_dotenv(dotenv_path="/workspace/siriusAI/temp1/project-root/src/latest_ai_development/.env")

# API_KEY = os.getenv("OPENROUTER_API_KEY")
# if not API_KEY:
#     raise ValueError("❌ OPENROUTER_API_KEY not loaded. Check your .env file path.")

# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# def summarize(topic):
#     """
#     Summarize AML-related content from scraped data using OpenRouter API and save AML report.
#     Reads scraped_data.json, processes summaries, and outputs aml_report.json.
#     """

#     print(f"[UTIL] Summarizing research on topic: {topic}")

#     # Check if scraped data exists
#     scraped_file = "output/scraped_data.json"
#     if not os.path.exists(scraped_file):
#         raise FileNotFoundError("❌ scraped_data.json not found. Run scraping first.")

#     with open(scraped_file, "r") as f:
#         scraped_results = json.load(f)

#     summaries = []
#     for idx, item in enumerate(scraped_results, start=1):
#         url = item.get("url")
#         content = item.get("content", "")

#         if not content.strip():
#             print(f"⚠️ Skipping {url}, no content found.")
#             continue

#         print(f"➡️ Summarizing content from URL {idx}/{len(scraped_results)}: {url}")
#         prompt = f"""You are a helpful assistant. Summarize the following article focusing ONLY on:
# - Money laundering
# - Financial fraud
# - Suspicious financial activities

# If nothing relevant is found, respond: "No relevant AML content found."

# ### URL:
# {url}

# ### Extracted Text:
# {content[:5000]}"""  # Increased to 2000 chars for better context

#         try:
#             # Call OpenRouter API
#             response = requests.post(
#                 API_URL,
#                 headers=HEADERS,
#                 json={
#                     "model": "meta-llama/llama-3-8b-instruct",  # You can change to another model
#                     "messages": [{"role": "user", "content": prompt}],
#                     "temperature": 0.3,
#                     "max_tokens": 800
#                 },
#                 timeout=180
#             )

#             if response.status_code != 200:
#                 raise Exception(f"API Error {response.status_code}: {response.text}")

#             output = response.json().get("choices", [])[0].get("message", {}).get("content", "").strip()
#             summaries.append({
#                 "url": url,
#                 "summary": output if output else "⚠️ No summary generated"
#             })
#             print(f"✅ Summary generated for {url}")

#         except Exception as e:
#             print(f"❌ Error summarizing {url}: {e}")
#             summaries.append({
#                 "url": url,
#                 "summary": f"Error: {e}"
#             })

#     # Save summaries to AML report file
#     aml_report = {
#         "topic": topic,
#         "total_urls": len(scraped_results),
#         "summaries": summaries
#     }

#     os.makedirs("output", exist_ok=True)
#     with open("output/aml_report.json", "w") as f:
#         json.dump(aml_report, f, indent=2)

#     print(f"[UTIL] ✅ AML report saved to output/aml_report.json")
#     return aml_report
