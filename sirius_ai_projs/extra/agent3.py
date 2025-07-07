import json
import requests
from pathlib import Path

print("✅ Agent 3 module loaded.")

# 🔧 LLM Config
graph_config = {
    "llm": {
        "model": "ollama/llama3.2:1b",
        "temperature": 0.7,
        "format": "json",
        "model_tokens": 2000,
        "base_url": "http://localhost:11434"
    }
}

def load_scraped_output(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_content(url, content):
    prompt = f"""You are a helpful assistant. Summarize the following article focusing ONLY on topics related to:
- Money laundering
- Financial fraud
- Suspicious financial activities

If nothing related is found, respond: "No relevant AML content found."

### URL:
{url}

### Extracted Text:
{content[:3000]}"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "temperature": 0.7,
                "stream": False,
                "num_predict": 1024
            },
            timeout=60
        )
        response.raise_for_status()
        output = response.json().get("response", "").strip()
        if not output:
            print(f"⚠️ Empty summary from model for URL: {url}")
            return "⚠️ LLM returned an empty summary."
        return output
    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        return f"❌ Error calling LLM: {e}"

# ✅ Refactored entry point for CrewAI
def run_agent3():
    input_json_path = r"D:\project\temp_project\agent2\output27.json"
    output_txt_path = "summary7.txt"
    input_dump_path = "summary_input7.txt"

    data = load_scraped_output(input_json_path)

    summaries = []
    summary_input_dump = []

    for idx, entry in enumerate(data, 1):
        url = entry.get("url")
        content = entry.get("content", "")
        error = entry.get("error", "")

        if error:
            print(f"⛔ Skipping due to error: {url} | Error: {error}")
            continue
        if "access denied" in content.lower():
            print(f"⛔ Skipping due to access restriction: {url}")
            continue
        if not content.strip():
            print(f"⛔ Skipping due to empty content: {url}")
            continue

        print(f"📝 [{idx}/{len(data)}] Summarizing: {url}")
        summary = summarize_content(url, content)

        if "No relevant AML content" not in summary:
            summaries.append(f"\n📌 URL: {url}\n{summary}\n")
        else:
            print(f"⚠️ No AML content found in: {url}")

        summary_input_dump.append(f"\n📌 URL: {url}\n\n{content[:4000]}...\n")

    Path(output_txt_path).write_text("\n".join(summaries), encoding="utf-8")
    Path(input_dump_path).write_text("\n".join(summary_input_dump), encoding="utf-8")

    print(f"\n✅ Final summaries saved to: {output_txt_path}")
    print(f"📎 Raw input dump saved to: {input_dump_path}")

# if __name__ == "__main__":
#     run_agent3()
