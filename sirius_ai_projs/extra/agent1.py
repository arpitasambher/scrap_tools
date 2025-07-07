import json
import os
import requests
import re
from dotenv import load_dotenv

print("✅ Agent 1 module loaded.")

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourdomain.com",
    "X-Title": "DataPermutationAgent"
}

def get_user_input():
    print("🔹 Enter the following details to generate realistic data permutations:")
    user_data = {
        "name": input("Name: "),
        "phone": input("Phone number: "),
        "paytm_link": input("Paytm link: "),
        "country": input("Country: "),
        "age": input("Age: "),
        "email": input("Email: ")
    }
    while True:
        try:
            num_permutations = int(input("Number of permutations to generate (e.g., 15): "))
            if num_permutations <= 0:
                raise ValueError
            break
        except ValueError:
            print("❌ Please enter a valid positive integer.")
    return user_data, num_permutations

def extract_json_block(text):
    match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
    return match.group(0) if match else None

def generate_permutations(user_input, num_permutations):
    prompt = f"""
You are an expert data variation generator. Given a dictionary of user data, your job is to produce exactly **{num_permutations} realistic permutations** of that data.

Each permutation MUST include changes in the **name field**. You must vary names in at least one of the following ways:
- Typo or keyboard error (e.g., "Vijay Mallaya" → "Vijya Malaya")
- Initials (e.g., "Vijay Mallaya" → "V. Mallaya")
- All caps or lowercase (e.g., "VIJAY MALLAYA", "vijay mallaya")
- First or last name swapped (e.g., "Mallaya Vijay")
- Extra or missing letters (e.g., "Vijjay", "Mallay")
- Dots, dashes, or alternate spacing (e.g., "V.Mallaya", "Vijay-M.")

Also include variations in:
- Phone number (e.g., +91 format, digit changes)
- Paytm link (format, domain, symbol changes)
- Email (username or domain typos)
- Country (misspelling or short form)
- Age (spacing, suffixes)
- Capitalization or spacing differences

⚠️ You MUST include a **name variation** in every entry. Do not leave the name identical in all entries.

### Input:
{json.dumps(user_input, indent=2)}

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

    body = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt.strip()}],
        "max_tokens": 4096,
        "temperature": 0.5
    }

    response = requests.post(API_URL, headers=HEADERS, data=json.dumps(body))

    if response.status_code != 200:
        print("❌ API Error:", response.text)
        exit()

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to extract response:", e)
        print("🔍 Raw:", response.text)
        exit()

def save_output(output_text, num_permutations, user_input, retry=False):
    try:
        clean_json = extract_json_block(output_text)
        if not clean_json:
            raise ValueError("No valid JSON array found.")
        data = json.loads(clean_json)

        if isinstance(data, list) and len(data) == num_permutations:
            with open("permuted_user_data27.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print("✅ Output saved to permuted_user_data27.json")
        else:
            print(f"⚠️ Received {len(data)} entries instead of {num_permutations}.")
            if not retry:
                print("🔁 Retrying once...")
                output_retry = generate_permutations(user_input, num_permutations)
                save_output(output_retry, num_permutations, user_input, retry=True)
            else:
                with open("output_debug27.txt", "w", encoding="utf-8") as f:
                    f.write(output_text)
                print("🛠 Raw output saved to output_debug27.txt")
    except Exception as e:
        print(f"❌ Output is not valid JSON. Error: {e}")
        with open("output_debug.txt", "w", encoding="utf-8") as f:
            f.write(output_text)
        print("🛠 Raw output saved to output_debug.txt")

# ✅ Refactored entry point for CrewAI
def run_agent1():
    user_input, num_permutations = get_user_input()
    with open("original_user_input.json", "w", encoding="utf-8") as f:
        json.dump(user_input, f, indent=2)

    output_text = generate_permutations(user_input, num_permutations)
    save_output(output_text, num_permutations, user_input)

# if __name__ == "__main__":
#      run_agent1()
