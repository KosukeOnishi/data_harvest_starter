import asyncio
import sys, os
from dotenv import load_dotenv
from pydantic import BaseModel
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai_client import async_client as client
import aiohttp

load_dotenv()
PPLX_API_KEY = os.getenv("PPLX_API_KEY")
url = "https://api.perplexity.ai/chat/completions"

class CityInfo(BaseModel):
    name: str
    description: str

def prepare_prompt_pplx(city):
    prompt = f"""
    Write a detailed explanation (around 200 words) of the city called “{city}”.
    """
    return prompt

def prepare_prompt_openai(description, city):
    prompt = f"""
    Generate a JSON object with the following fields for a city based on the details below. Make sure to explain the information in your own words and avoid copying directly from the provided text
    - name: The name of the city.
    - description: A detailed description around 80 words, divided into two paragraphs. Separate paragraphs using \\n.

    Use the following information:
    city name: {city}
    description: {description}
    """
    return prompt

async def post_request(url, payload, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            return await response.text()

async def send_request(payload, headers, index, size, city):
    try:
        response_text = await post_request(url, payload, headers)

        data = json.loads(response_text)

        usage = data["usage"]
        description = data["choices"][0]["message"]["content"]
        print(f"Consumed Tokens: {usage['total_tokens']} (in {usage['prompt_tokens']}, out {usage['completion_tokens']})")

        prompt = prepare_prompt_openai(description, city)
        messages = [
            {
                "role": "user",
                "content": (
                    prompt
                )
            }
        ]

        completion = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
            response_format=CityInfo,
            max_tokens=1000,
            n=1,
        )
        usage = completion.usage
        print(f"Request Completed ✅️ ({index}/{size}): {usage.total_tokens} (in {usage.prompt_tokens}, out {usage.completion_tokens})")
        data = completion.choices[0].message.parsed
        data = {
            "name": data.name,
            "description": data.description,
        }
        # output as json
        with open(f'{index}.json', 'w') as f:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            f.write(json_data)
            f.close()
    except Exception as e:
        with open(f'{index}_error.json', 'w') as f:
            json_data = json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
            f.write(json_data)
            f.close()

async def main():
    cities = ['New York', 'London', 'Tokyo', 'Paris', 'Berlin']

    tasks = []
    for i, city in enumerate(cities, 1):
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "user",
                    "content": prepare_prompt_pplx(city)
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

        task = asyncio.create_task(send_request(payload, headers, i, len(cities), city))
        tasks.append(task)

        print(f"Request sent: {i}/{len(cities)}")

        # Be careful not to exceed the rate/tokens limit.
        await asyncio.sleep(1)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
