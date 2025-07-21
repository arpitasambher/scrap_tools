


import os
import json
from crewai_tools import ScrapeWebsiteTool

def scrape_all():
    """
    Scrape all URLs from search_results.json and save results to scraped_data.json.
    Uses ScrapeWebsiteTool for actual scraping.
    """

    # Load search results
    if not os.path.exists("output/search_data.json"):
        raise FileNotFoundError("❌ search_data.json not found in output folder.")

    with open("output/search_data.json", "r") as f:
        search_data = json.load(f)

    scraped_data = []
    print(f"🕷 Starting scraping for {len(search_data)} URLs...")

    for idx, result in enumerate(search_data, start=1):
        url = result.get("link")
        if not url:
            print(f"⚠️ Skipping entry {idx}, no URL found.")
            continue

        print(f"➡️ Scraping ({idx}/{len(search_data)}): {url}")
        try:
            tool = ScrapeWebsiteTool(website_url=url)
            content = tool.run()

            if content and content.strip():
                trimmed_content = content.strip()[:3000]  # ⛔ Trim to first 3000 characters

                scraped_data.append({
                    "url": url,
                    "content": trimmed_content
                })
                print(f"✅ Scraped {len(trimmed_content)} characters (trimmed).")

            else:
                scraped_data.append({
                    "url": url,
                    "error": "Empty content"
                })
                print("⚠️ Empty or no content.")

        except Exception as e:
            scraped_data.append({
                "url": url,
                "error": str(e)
            })
            print(f"❌ Error scraping {url}: {e}")

    # Save scraped data to file
    os.makedirs("output", exist_ok=True)
    with open("output/scraped_data.json", "w") as f:
        json.dump(scraped_data, f, indent=2)

    print(f"✅ Saved {len(scraped_data)} scraped pages to output/scraped_data.json")
    return scraped_data
