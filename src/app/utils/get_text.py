from pypdf import PdfReader
from pathlib import Path


def get_PDF_text(file: str):
    text = ""

    # Read the PDF file and extract text
    try:
        with Path(file).open("rb") as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        raise ValueError(f"Error reading the PDF file: {str(e)}")

        # Check if the PDF has more than ~400,000 characters
        # The context length limit of the model is 131,072 tokens and thus the text should be less
        # than this limit
        # Assumes that 1 token is approximately 4 characters
    if len(text) > 400000:
        raise ValueError(
            "The PDF is too long. Please upload a PDF with fewer than ~131072 tokens."
        )

    return text

    text = get_PDF_text("MoA.pdf")
