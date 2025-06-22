from together import Together
from core.config import settings
from pydantic import ValidationError

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


def generate_script(system_prompt: str, input_text: str, output_model):
    try:
        response = call_llm(system_prompt, input_text, output_model)
        dialogue = output_model.model_validate_json(response)
    except ValidationError as e:
        error_message = f"Failed to parse dialogue JSON: {e}"
        system_prompt_with_error = f"{system_prompt}\n\nPlease return a VALID JSON object. This was the earlier error: {error_message}"
        response = call_llm(system_prompt_with_error, input_text, output_model)
        dialogue = output_model.model_validate_json(response)
    return dialogue
