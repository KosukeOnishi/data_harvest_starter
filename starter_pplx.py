import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
PPLX_API_KEY = os.getenv("PPLX_API_KEY")
url = "https://api.perplexity.ai/chat/completions"

def main():
    prompt = """
    Search for the weather forecast for Tokyo tomorrow.
    """

    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.4,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    response_text = response.text

    data = json.loads(response_text)

    usage = data["usage"]
    print(f"Consumed Tokens: {usage['total_tokens']} (in {usage['prompt_tokens']}, out {usage['completion_tokens']})")
    print(data["choices"][0]["message"])

if __name__ == "__main__":
    main()