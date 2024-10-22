import asyncio
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai_client import async_client as client

def prepare_prompt(city):
    return f"""
    Describe the city less than 100 words.
    city: {city}
    """

# This function sends a request to the OpenAI API.
async def send_request(messages, index, size):
    try:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
            n=1,
        )
        usage = completion.usage
        print(f"Request Completed ✅️ ({index}/{size}): {usage.total_tokens} (in {usage.prompt_tokens}, out {usage.completion_tokens})")
        print(f"{completion.choices[0].message.content}\n")
    except Exception as e:
        print(f"{e}")

async def main():
    tasks = []

    # sample data
    cities = ['New York', 'London', 'Tokyo', 'Paris', 'Berlin']

    for i, city in enumerate(cities, 1):
        messages = [
            {
                "role": "user",
                "content": (
                    prepare_prompt(city)
                )
            }
        ]

        task = asyncio.create_task(send_request(messages, i, len(cities)))
        tasks.append(task)

        print(f"Request sent: {i}/{len(cities)}")

        # Be careful not to exceed the rate/tokens limit.
        await asyncio.sleep(1)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
