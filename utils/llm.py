import os
import requests
from dotenv import load_dotenv
from together import Together

client = Together(api_key=os.getenv("TOKEN"))

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOKEN")


async def generate_story(prompt: str) -> str:

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
    )

    if response:
        return response.choices[0].message.content.strip()
    else:
        return "Ошибка генерации истории. Попробуйте позже."


async def generate_story1(prompt: str) -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Ошибка генерации истории. Попробуйте позже."
