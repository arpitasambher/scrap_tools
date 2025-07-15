import json
import os

def run_search(limit=10):
    """Mock search results for testing."""
    results = []
    for i in range(limit):
        results.append({
            "title": f"Result {i}",
            "link": f"http://example.com/{i}",
            "snippet": f"Snippet for result {i}"
        })

    os.makedirs("output", exist_ok=True)
    with open("output/search_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"[UTIL] ✅ Saved {len(results)} search results")
    return results
