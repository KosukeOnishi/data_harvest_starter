import base64
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai_client import client

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def main():
    base64_image = encode_image('data/sample/sample.png')

    prompt = """
    Describe the given image.
    """

    messages = [
        {
            "role": "user",
            "content": (
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "low"
                    },
                }
            )
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000,
        n=1
    )

    usage = completion.usage
    print(f"Consumed Tokens: {usage.total_tokens} (in {usage.prompt_tokens}, out {usage.completion_tokens})")
    print(completion.choices[0].message)

if __name__ == "__main__":
    main()
