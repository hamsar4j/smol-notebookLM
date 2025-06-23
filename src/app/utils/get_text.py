from pypdf import PdfReader
from pathlib import Path


def get_PDF_text(file: str):
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
