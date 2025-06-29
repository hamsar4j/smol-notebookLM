from app.llm.router import call_llm
from pydantic import ValidationError
from app.utils.get_text import get_PDF_text
from app.models.models import Transcript
from app.tts.tts_bytes import generate_audio_from_script, concatenate_audio_files
from app.llm.prompts import SYSTEM_PROMPT
import json
import logging

logger = logging.getLogger(__name__)


def create_script_from_pdf(
    pdf_path: str, system_prompt: str = SYSTEM_PROMPT
) -> Transcript:
    """Reads a PDF and generates a script using an LLM."""
    text = get_PDF_text(pdf_path)
    logger.info(f"Extracted text from PDF: {len(text)} characters")
    script_obj = generate_script(system_prompt, text, Transcript)
    logger.info(f"Generated script: {script_obj}")
    return script_obj


def save_script_to_json(script_obj, filename: str) -> None:
    """Saves the script object to a JSON file."""
    script_dict = {"response": script_obj.model_dump()}
    with open(filename, "w") as f:
        json.dump(script_dict, f, indent=2)
    logger.info(f"Script saved to {filename}")
    print(f"Script saved to {filename}")


def generate_script(system_prompt: str, input_text: str, output_model) -> Transcript:
    """Generates a script from the input text using an LLM."""
    try:
        logger.info("Calling LLM to generate script...")
        response = call_llm(system_prompt, input_text, output_model)
        dialogue = output_model.model_validate_json(response)
    except ValidationError as e:
        error_message = f"Failed to parse dialogue JSON: {e}"
        logger.error(error_message)
        system_prompt_with_error = f"{system_prompt}\n\nPlease return a VALID JSON object. This was the earlier error: {error_message}"
        response = call_llm(system_prompt_with_error, input_text, output_model)
        dialogue = output_model.model_validate_json(response)
    return dialogue


def create_and_concatenate_audio(
    script: list, output_filename: str = "full_podcast.wav"
) -> str:
    """Generates audio files from a script and concatenates them."""
    audio_files = generate_audio_from_script(script)
    concatenate_audio_files(audio_files, output_filename)
    return output_filename
