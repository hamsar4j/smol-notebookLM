from together import Together
from typing import Optional, Any
from app.core.config import settings

# client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
client = Together(api_key=settings.llm_api_key)


def call_llm(system_prompt: str, text: str, format: Optional[Any] = None) -> str:

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "model": settings.llm_model,
        "max_tokens": settings.llm_max_tokens,
    }

    if format:
        payload["response_format"] = {
            "type": "json_object",
            "schema": format.model_json_schema(),
        }

    response = client.chat.completions.create(**payload)
    return response.choices[0].message.content if response.choices else ""
