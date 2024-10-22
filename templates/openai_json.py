import sys
import os
from pydantic import BaseModel
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai_client import client

def main():
    class OpenAIUsecases(BaseModel):
        class OpenAIUsecase(BaseModel):
            name: str
            description: str
            api_endpoint: str

        usecases: List[OpenAIUsecase]

    prompt = """
    “Imagine you are an expert in leveraging AI through OpenAI's API. I want you to come up with various practical and innovative use cases where the API can be applied.
    Return the results in JSON format. The parameters are defined as follows:
    usecases: a list of use cases
    name: the name of the use case
    description: a brief description of the use case
    api_endpoint: the API endpoint to use for the use case
    """

    messages = [
        {
            "role": "system",
            "content": "You are a technical assistant who specializes in programming, especially in providing guidance for using APIs, writing efficient code, and troubleshooting."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=OpenAIUsecases,
        max_tokens=1000,
        n=1
    )

    usage = completion.usage
    # automatically parsed into OpenAIUsecases
    usecases = completion.choices[0].message.parsed

    print(f"Consumed Tokens: {usage.total_tokens} (in {usage.prompt_tokens}, out {usage.completion_tokens})")
    print(completion.choices[0].message.parsed)

if __name__ == "__main__":
    main()
