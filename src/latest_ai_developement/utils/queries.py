import json
import os
import random

def generate_queries(permutations, queries_per_identity=5):
    keywords = ["money laundering", "financial crime", "fraud"]
    queries = []
    for data in permutations:
        for _ in range(queries_per_identity):
            q = f"{data['name']} {data['country']} {random.choice(keywords)}"
            queries.append({"query": q})

    os.makedirs("output", exist_ok=True)
    with open("output/queries.json", "w") as f:
        json.dump(queries, f, indent=2)
    print(f"[UTIL] ✅ Saved {len(queries)} queries")
    return queries
