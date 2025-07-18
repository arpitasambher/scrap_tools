# import json
# import os

# def scrape_all():
#     """Mock scraping logic."""
#     with open("output/search_results.json") as f:
#         search_results = json.load(f)

#     scraped_data = []
#     for result in search_results:
#         scraped_data.append({
#             "url": result["link"],
#             "content": f"Sample content from {result['link']}"
#         })

#     os.makedirs("output", exist_ok=True)
#     with open("output/scraped_data.json", "w") as f:
#         json.dump(scraped_data, f, indent=2)
#     print(f"[UTIL] ✅ Saved {len(scraped_data)} scraped pages")
#     return scraped_data


import os
import json
from crewai_tools import ScrapeWebsiteTool

def scrape_all():
    """
    Scrape all URLs from search_results.json and save results to scraped_data.json.
    Uses ScrapeWebsiteTool for actual scraping.
    """

    # Load search results
    if not os.path.exists("output/search_results.json"):
        raise FileNotFoundError("❌ search_results.json not found in output folder.")

    with open("output/search_results.json", "r") as f:
        search_results = json.load(f)

    scraped_data = []
    print(f"🕷 Starting scraping for {len(search_results)} URLs...")

    for idx, result in enumerate(search_results, start=1):
        url = result.get("link")
        if not url:
            print(f"⚠️ Skipping entry {idx}, no URL found.")
            continue

        print(f"➡️ Scraping ({idx}/{len(search_results)}): {url}")
        try:
            tool = ScrapeWebsiteTool(website_url=url)
            content = tool.run()

            if content and content.strip():
                scraped_data.append({
                    "url": url,
                    "content": content.strip()
                })
                print(f"✅ Scraped {len(content)} characters.")
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
