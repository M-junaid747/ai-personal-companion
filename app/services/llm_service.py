import os
from groq import AsyncGroq

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def get_groq_reply(messages: list, model: str = "llama3-8b-8192") -> str:
    response = await client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return response.choices[0].message.content