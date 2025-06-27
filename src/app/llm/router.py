from together import Together
from core.config import settings

# client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
client = Together(api_key=settings.llm_api_key)


def call_llm(system_prompt: str, text: str, dialogue_format) -> str:

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        model=settings.llm_model,
        max_tokens=200000,
        response_format={
            "type": "json_object",
            "schema": dialogue_format.model_json_schema(),
        },
    )
    return response.choices[0].message.content if response.choices else ""
