from app.llm.router import call_llm
from pydantic import ValidationError
from app.utils.get_text import load_pdf_text, save_pdf_text
from app.models.models import Transcript, ChatResponse
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

    pdf_filename = os.path.basename(pdf_path)
    save_pdf_text(pdf_path, pdf_filename)

    text = load_pdf_text(pdf_filename)
    logger.info(f"Using PDF text: {len(text)} characters")

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
        script = output_format.model_validate_json(response)
    except ValidationError as e:
        error_message = f"Failed to parse script JSON: {e}"
        logger.error(error_message)
        system_prompt_with_error = f"""
        {system_prompt}\n\nPlease return a VALID JSON object. This was the earlier error: {error_message}
        """
        response = call_llm(system_prompt_with_error, input_text, output_format)
        script = output_format.model_validate_json(response)
    return script


def build_audio_from_script(script: dict) -> str:
    """Generates audio files from a script and concatenates them into a single file."""

    output_filename = os.path.join(AUDIO_DIR, "full_podcast.wav")

    audio_files = generate_audio_from_script(script, output_dir=AUDIO_DIR)
    concatenate_audio_files(audio_files, output_filename)
    return output_filename


def chat_with_pdf_content(pdf_filename: str, user_message: str) -> ChatResponse:
    """Chat with LLM using stored PDF content as context."""
    try:
        # Load the extracted text from storage
        pdf_text = load_pdf_text(pdf_filename)
        logger.info(f"Using stored PDF text for chat: {len(pdf_text)} characters")
    except FileNotFoundError:
        raise FileNotFoundError(f"No extracted text found for PDF: {pdf_filename}")

    if not pdf_text.strip():
        raise ValueError("No text content available for this PDF")

    # Create context-aware prompt
    context_prompt = f"""
    You are a helpful AI assistant. The user has uploaded a PDF document and wants to chat about its contents. 
    
    Here is the content of the PDF:
    
    {pdf_text}
    
    Please answer the user's question based on the PDF content. If the question cannot be answered from the PDF content, 
    let the user know and provide general guidance if possible.
    """

    response = call_llm(context_prompt, user_message)

    return ChatResponse(response=response)
