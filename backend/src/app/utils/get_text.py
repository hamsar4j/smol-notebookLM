from pypdf import PdfReader
from pathlib import Path
from app.core.constants import TEXT_DIR
import logging
import os
import json

logger = logging.getLogger(__name__)


def get_text_filename(pdf_filename: str) -> str:
    """Generate text filename from PDF filename."""
    pdf_name = Path(pdf_filename).stem
    return f"{pdf_name}.json"


def save_pdf_text(pdf_path: str, pdf_filename: str) -> str:
    """Extract text from PDF and save to storage."""
    text_filename = get_text_filename(pdf_filename)
    text_path = os.path.join(TEXT_DIR, text_filename)

    # Check if text file already exists
    if os.path.exists(text_path):
        logger.info(f"Text file already exists: {text_path}")
        return text_path

    try:
        extracted_text = get_PDF_text(pdf_path)

        text_data = {
            "pdf_filename": pdf_filename,
            "pdf_path": pdf_path,
            "extracted_text": extracted_text,
            "extraction_date": str(Path(pdf_path).stat().st_mtime),
        }

        with open(text_path, "w", encoding="utf-8") as f:
            json.dump(text_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Saved extracted text to: {text_path}")
        return text_path

    except Exception as e:
        logger.error(f"Failed to extract and save text from {pdf_path}: {e}")
        raise


def load_pdf_text(pdf_filename: str) -> str:
    """Load extracted text from storage."""
    text_filename = get_text_filename(pdf_filename)
    text_path = os.path.join(TEXT_DIR, text_filename)

    if not os.path.exists(text_path):
        raise FileNotFoundError(f"Text file not found: {text_path}")

    try:
        with open(text_path, "r", encoding="utf-8") as f:
            text_data = json.load(f)
            return text_data.get("extracted_text", "")
    except Exception as e:
        logger.error(f"Failed to load text from {text_path}: {e}")
        raise


def text_exists(pdf_filename: str) -> bool:
    """Check if extracted text exists for a PDF."""
    text_filename = get_text_filename(pdf_filename)
    text_path = os.path.join(TEXT_DIR, text_filename)
    return os.path.exists(text_path)


def get_PDF_text(file: str) -> str:
    text = ""

    try:
        with Path(file).open("rb") as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        raise ValueError(f"Error reading the PDF file: {str(e)}")

    # Assumes that 1 token is approximately 4 characters
    if len(text) > 400000:
        raise ValueError(
            "The PDF is too long. Please upload a PDF with fewer than ~131072 tokens."
        )

    return text
