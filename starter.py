from openai_client import client

def main():
    prompt = """
    Can you provide a brief overview of how to make the most out of OpenAI API for a project?
    """

    messages = [
        {
            "role": "system",
            "content": "You are a technical assistant who specializes in programming, especially in providing guidance for using APIs, writing efficient code, and troubleshooting."
        },
        {
            "role": "user",
            "content": (
                prompt
            )
        }
    ]

    # Please refer to the following link for information about models and limits
    # https://platform.openai.com/settings/organization/limits
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
