import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Create OpenAI client (THIS WAS MISSING)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set")


async def analyze_image(image_url: str, prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content
