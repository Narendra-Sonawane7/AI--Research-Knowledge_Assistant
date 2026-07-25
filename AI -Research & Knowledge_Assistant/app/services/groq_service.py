from groq import Groq
from app.config import settings


def get_client():
    if not settings.GROQ_API_KEY:
        return None
    return Groq(api_key=settings.GROQ_API_KEY)


def ask_groq(system_prompt: str, user_prompt: str) -> str:
    client = get_client()
    if client is None:
        return "GROQ_API_KEY is missing. Add it to your .env file."

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
