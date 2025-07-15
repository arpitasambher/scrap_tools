import json
import os

def scrape_all():
    """Mock scraping logic."""
    with open("output/search_results.json") as f:
        search_results = json.load(f)

    scraped_data = []
    for result in search_results:
        scraped_data.append({
            "url": result["link"],
            "content": f"Sample content from {result['link']}"
        })

    os.makedirs("output", exist_ok=True)
    with open("output/scraped_data.json", "w") as f:
        json.dump(scraped_data, f, indent=2)
    print(f"[UTIL] ✅ Saved {len(scraped_data)} scraped pages")
    return scraped_data
