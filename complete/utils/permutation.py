
import os
import re
import json
from typing import List
from pydantic import BaseModel
from google import generativeai as genai

# ==== Step 1: Configure Gemini API ====
# Optionally set key here or use dotenv
os.environ["GEMINI_API_KEY"] = "AIzaSyDtEU5NR-019IdaTWDQznKNxlbUvRo7bUY"  # Replace with your actual key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ==== Step 2: Pydantic Model ====
class Permutation(BaseModel):
    name: str
    phone: str
    paytm_link: str
    country: str
    age: str
    email: str

# ==== Step 3: Generate Permutations ====
def generate_permutations(user_data: dict, num: int) -> List[Permutation]:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
You are an expert data variation generator. Generate exactly {num} realistic permutations of this user data:

{json.dumps(user_data)}

Each permutation must:
- Vary the name (typos, initials, case, swapped, spacing, etc.)
- Vary at least one other field: phone, email, paytm_link, country, or age.

Output MUST be a JSON array, like:
[
  {{
    "name": "string",
    "phone": "string",
    "paytm_link": "string",
    "country": "string",
    "age": "string",
    "email": "string"
  }},
  ...
]
Use only double quotes and no extra text or markdown.
"""

    response = model.generate_content(prompt)
    raw = response.text

    # Cleanup: remove markdown or backticks if present
#     raw = re.sub(r"```[\s\S]*?```", "", raw).strip()
    raw = re.sub(r"^```json|```$", "", raw.strip(), flags=re.IGNORECASE).strip()
    # Parse response
    try:
        json_data = json.loads(raw)
        permutations = [Permutation(**entry) for entry in json_data]
    except Exception as e:
        print("❌ Error parsing Gemini output:", e)
        print("Raw response:\n", raw)
        return []

    # ==== Step 4: Save to File ====
    output_path =  "/workspace/siriusAI/scrap_tools-main/scrap_tools-main/final/output/permuted_data.json"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump([p.model_dump() for p in permutations], f, indent=2)
        print(f"[✅] Saved {len(permutations)} permutations to: {output_path}")
        
#     for i, p in enumerate(res, 1):
#         print(f"\n✅ Permutation {i}:\n{p.model_dump_json(indent=2)}")
    print("PRINT THE VALUE :")
    print(permutations)
    return permutations
