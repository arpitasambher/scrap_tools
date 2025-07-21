
import json
import os
import random
import re

def clean_text(text):
    return re.sub(r"[`]", "", text.strip())

def generate_queries(permutations, queries_per_identity=5):
    keywords = ["money laundering", "financial crime", "fraud"]
    queries = []

    for data in permutations:
        name = clean_text(data.get("name", ""))
        country = clean_text(data.get("country", ""))
        for _ in range(queries_per_identity):
            q = f"{name} {country} {random.choice(keywords)}"
            queries.append({"query": q})

    
    print("[DEBUG] Sample query:", queries[0] if queries else "No queries")


    # Write JSON safely
    output_path =  "/workspace/siriusAI/scrap_tools-main/scrap_tools-main/final/output/queries_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(queries, f, indent=2)

    print(f"[UTIL] ✅ Saved {len(queries)} queries to {output_path}")
    return queries
