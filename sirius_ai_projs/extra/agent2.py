import os
import json
from dotenv import load_dotenv
from serpapi import GoogleSearch
from crewai_tools import ScrapeWebsiteTool

print("✅ Agent 2 module loaded.")

# Load environment variables
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

# -------------------------------
# Step 1: Load permutations & generate queries
# -------------------------------
def load_and_generate_queries(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    queries = []
    for entry in data:
        name = entry["name"].strip()
        country = entry["country"].strip()
        phone = entry["phone"].strip()
        email = entry["email"].strip()
        age = entry["age"].strip()

        query = f"{name} , ANTI money laundering , {country} {phone} {email} {age}"
        queries.append((entry, query))
    return queries

# -------------------------------
# Step 2: Perform Serper search and collect top 15 links
# -------------------------------
def get_top_15_urls(query: str) -> list:
    if not SERP_API_KEY:
        raise ValueError("❌ SERP_API_KEY not found in .env file")

    print(f"\n🔍 Searching for query: {query}")
    all_urls = set()

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
                if link:
                    print(f"🔗 URL found: {link}")
                    all_urls.add(link)
                if len(all_urls) >= 15:
                    print("🚦 Reached 15 URL limit. Stopping early.")
                    break

        except Exception as e:
            print(f"❌ Error during {search_type} search: {e}")

    print(f"🧾 Total unique URLs collected: {len(all_urls)}\n")
    return list(all_urls)[:15]

# -------------------------------
# Step 3: Scrape URLs using ScrapeWebsiteTool
# -------------------------------
def scrape_with_scrapewebsite_tool(urls: list) -> list:
    scraped_results = []

    for idx, url in enumerate(urls):
        print(f"\n🕷 Scraping URL {idx+1}/{len(urls)}: {url}")
        try:
            tool = ScrapeWebsiteTool(website_url=url)
            content = tool.run()

            if content and content.strip():
                scraped_results.append({
                    "url": url,
                    "content": content.strip()
                })
                print(f"✅ Scraped {len(content)} characters.")
            else:
                print("⚠️ Empty or no content.")
                scraped_results.append({
                    "url": url,
                    "error": "Empty content"
                })

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            scraped_results.append({
                "url": url,
                "error": str(e)
            })

    return scraped_results

# ✅ Refactored entry point for CrewAI
def run_agent2():
    json_path = r"D:\project\temp_project\agent1\permuted_user_data27.json"
    results = load_and_generate_queries(json_path)

    all_urls = set()
    print("\n🚀 Running SerpAPI queries...\n")
    for idx, (entry, query) in enumerate(results):
        print(f"\n🔎 Query {idx+1}:\n{query}")
        urls = get_top_15_urls(query)
        print(f"🔗 Found {len(urls)} URLs.")
        all_urls.update(urls)

    all_urls = list(all_urls)[:10]
    print(f"\n🌐 Total unique URLs to scrape: {len(all_urls)}")

    scraped_data = scrape_with_scrapewebsite_tool(all_urls)

    with open("output27.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2)

    print(f"\n✅ Saved {len(scraped_data)} scraped entries to output27.json")

# if __name__ == "__main__":
#     run_agent2()
