


import os
import json
from pathlib import Path
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Absolute path to your .env file
env_path = Path("/workspace/siriusAI/temp1/project-root/src/latest_ai_development/.env")

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Assign SERP API key
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Check if keys loaded

print("SERP_API_KEY:", SERP_API_KEY)

def run_search(query, limit=15):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/workspace/siriusAI/temp1/project-root/src/latest_ai_development/.env")
    SERP_API_KEY = os.getenv("SERP_API_KEY")

    if not SERP_API_KEY:
        raise ValueError("❌ SERP_API_KEY not found in .env file")


    print(f"\n🔍 Starting search for query: {query}")
    all_urls = set()
    results_data = []

    for search_type in ["search", "news"]:
        print(f"➡️ Running {search_type} search...")

        params = {
            "api_key": SERP_API_KEY,
            "engine": "google",
            "q": query,
            "type": search_type,
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en"
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            print(f"✅ Got response for {search_type} search.")

            organic_results = results.get("organic_results", [])
            print(f"🔎 Found {len(organic_results)} organic results in {search_type} search.")

            for result in organic_results:
                link = result.get("link")
                title = result.get("title", "No Title")
                snippet = result.get("snippet", "No Snippet")

                if link and link not in all_urls:
                    all_urls.add(link)
                    results_data.append({"title": title, "link": link, "snippet": snippet})
                    print(f"🔗 Added: {link}")

                if len(all_urls) >= limit:
                    print("🚦 Reached URL limit. Stopping early.")
                    break

        except Exception as e:
            print(f"❌ Error during {search_type} search: {e}")

        if len(all_urls) >= limit:
            break

    # Save to file
    os.makedirs("output", exist_ok=True)
    with open("output/search_data.json", "w") as f:
        json.dump(results_data, f, indent=2)

    print(f"✅ Saved {len(results_data)} search results to output/search_data.json")
    return results_data
