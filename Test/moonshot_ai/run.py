import os
from openai import OpenAI

# Get API key from environment variable
api_key = os.getenv('MOONSHOT_API_KEY')
if not api_key:
    raise ValueError("Please set the MOONSHOT_API_KEY environment variable")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.ai/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "You are Kimi, an AI assistant provided by Moonshot AI. You are proficient in Chinese and English conversations. You provide users with safe, helpful, and accurate answers. You will reject any questions involving terrorism, racism, or explicit content. Moonshot AI is a proper noun and should not be translated."},
            {"role": "user", "content": "Hello, my name is adarsh. What is 1+1?"}
        ],
        temperature=0.3,
    )

    print(completion.choices[0].message.content)

except Exception as e:
    print(f"Error occurred: {str(e)}")