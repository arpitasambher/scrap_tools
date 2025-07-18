# import json
# import os
# import requests

# API_URL = "https://openrouter.ai/api/v1/chat/completions"
# HEADERS = {
#     "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#     "Content-Type": "application/json"
# }

# def generate_permutations(user_data, num):
#     """
#     Generate realistic permutations of user-provided data using OpenRouter API.
#     Saves permutations to output/permuted_user_data.json and returns as a list.
#     """

#     # Build the prompt
#     prompt = f"""
# You are an expert data variation generator. Given a dictionary of user data, your job is to produce exactly **{num} realistic permutations** of that data.

# Each permutation MUST include changes in the **name field**. You must vary names in at least one of the following ways:
# - Typo or keyboard error
# - Initials (e.g., "V. Mallaya")
# - All caps or lowercase
# - First or last name swapped
# - Extra or missing letters
# - Dots, dashes, or alternate spacing

# Also include variations in:
# - Phone number
# - Paytm link
# - Email
# - Country
# - Age
# - Capitalization or spacing differences

# ⚠️ Include a name variation in every entry.

# ### Input:
# {json.dumps(user_data, indent=2)}

# ### Output Format:
# A JSON list like:
# [
#   {{
#     "name": "...",
#     "phone": "...",
#     "paytm_link": "...",
#     "country": "...",
#     "age": "...",
#     "email": "..."
#   }},
#   ...
# ]

# Respond with **only the JSON list**. No extra explanation.
# """

#     # Prepare API body
#     body = {
#         "model": "meta-llama/llama-3-8b-instruct",
#         "messages": [{"role": "user", "content": prompt.strip()}],
#         "max_tokens": 4096,
#         "temperature": 0.5
#     }

#     # API Request
#     print("[UTIL] Calling OpenRouter API for permutations...")
#     response = requests.post(API_URL, headers=HEADERS, data=json.dumps(body))

#     if response.status_code != 200:
#         print(f"❌ API Error: {response.status_code} - {response.text}")
#         return []

#     try:
#         raw_output = response.json()["choices"][0]["message"]["content"]
#         permutations = json.loads(raw_output)

#         # Ensure output directory exists
#         os.makedirs("output", exist_ok=True)

#         # Save to file
#         with open("output/permuted_user_data.json", "w") as f:
#             json.dump(permutations, f, indent=2)

#         print(f"[UTIL] ✅ Saved {len(permutations)} permutations to output/permuted_user_data.json")
#         return permutations

#     except Exception as e:
#         print(f"❌ Failed to parse API response: {e}")
#         print("🔍 Raw Response:", response.text)
#         return []


import json
import os
import requests
from dotenv import load_dotenv
import sys


# Correct path to the .env file (relative or absolute)
env_path = os.path.abspath("scrap_tools/final/.env")
print(env_path)
print("*"*100)
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
print(API_KEY)
print("*"*100)

if not API_KEY:
    raise ValueError("❌ API key not loaded. Check your .env file path and key name.")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_permutations(user_data, num):
    """
    Generate realistic permutations of user-provided data using OpenRouter API.
    Saves permutations to output/permuted_user_data.json and returns as a list.
    """

    # Build the prompt
    prompt = f"""
    You are an expert data variation generator. Given a dictionary of user data, your job is to produce exactly **{num} realistic permutations** of that data.

    Each permutation MUST include changes in the **name field**. You must vary names in at least one of the following ways:
    - Typo or keyboard error
    - Initials (e.g., "V. Mallaya")
    - All caps or lowercase
    - First or last name swapped
    - Extra or missing letters
    - Dots, dashes, or alternate spacing

    Also include variations in:
    - Phone number
    - Paytm link
    - Email
    - Country
    - Age
    - Capitalization or spacing differences

    ⚠️ Include a name variation in every entry.

    ### Input:
    {json.dumps(user_data, indent=2)}

    ### Output Format:
    A JSON list like:
    [
    {{
        "name": "...",
        "phone": "...",
        "paytm_link": "...",
        "country": "...",
        "age": "...",
        "email": "..."
    }},
    ...
    ]

    Respond with **only the JSON list**. No extra explanation.
    """

    # Prepare API body
    body = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt.strip()}],
        "max_tokens": 4096,
        "temperature": 0.5
    }

    # API Request
    print("[UTIL] Calling OpenRouter API for permutations...")
    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(body))

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code} - {response.text}")
        return []

    try:
        raw_output = response.json()["choices"][0]["message"]["content"]
        permutations = json.loads(raw_output)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        # Save to file
        with open("scrap_tools/final/output/permuted_user_data.json", "w") as f:
            json.dump(permutations, f, indent=2)

        print(f"[UTIL] ✅ Saved {len(permutations)} permutations to output/permuted_user_data.json")
        return permutations

    except Exception as e:
        print(f"❌ Failed to parse API response: {e}")
        print("🔍 Raw Response:", response.text)
        return []

if __name__ == "__main__":
    result = generate_permutations(
        user_data={
            "name": "John Doe",
            "phone": "+1234567890",
            "paytm_link": "paytm://1234567890",
            "country": "USA",
            "age": 30,
            "email": "test@email"
        }, num=12
    )

    print(result)