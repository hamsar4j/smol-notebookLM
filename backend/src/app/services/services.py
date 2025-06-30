from app.llm.router import call_llm
from pydantic import ValidationError
from app.utils.get_text import get_PDF_text
from app.models.models import Transcript
from app.tts.tts_bytes import generate_audio_from_script, concatenate_audio_files
from app.llm.prompts import SYSTEM_PROMPT
from app.core.constants import AUDIO_DIR
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)


def create_script_from_pdf(
    pdf_path: str, system_prompt: str = SYSTEM_PROMPT
) -> Transcript:
    """Reads a PDF and generates a script using an LLM."""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text = get_PDF_text(pdf_path)
    logger.info(f"Extracted text from PDF: {len(text)} characters")

    if not text.strip():
        raise ValueError("No text extracted from PDF")

    script_obj = generate_script(system_prompt, text, Transcript)
    logger.info(f"Generated script: {script_obj}")
    return script_obj


def generate_script(system_prompt: str, input_text: str, output_format) -> Transcript:
    """Generates a script from the input text using an LLM."""
    if not input_text.strip():
        raise ValueError("Input text cannot be empty")

    try:
        logger.info("Calling LLM to generate script...")
        response = call_llm(system_prompt, input_text, output_format)
        dialogue = output_format.model_validate_json(response)
    except ValidationError as e:
        error_message = f"Failed to parse dialogue JSON: {e}"
        logger.error(error_message)
        system_prompt_with_error = f"{system_prompt}\n\nPlease return a VALID JSON object. This was the earlier error: {error_message}"
        response = call_llm(system_prompt_with_error, input_text, output_format)
        dialogue = output_format.model_validate_json(response)
    return dialogue


def build_audio_from_script(script: dict, output_filename: str = None) -> str:
    """Generates audio files from a script and concatenates them into a single file."""
    if output_filename is None:
        output_filename = os.path.join(AUDIO_DIR, "full_podcast.wav")

    audio_files = generate_audio_from_script(script, output_dir=AUDIO_DIR)
    concatenate_audio_files(audio_files, output_filename)
    return output_filename
