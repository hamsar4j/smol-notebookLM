import json
from fastapi import FastAPI
from services.services import (
    create_script_from_pdf,
    save_script_to_json,
    create_and_concatenate_audio,
)

app = FastAPI(title="SMOL NotebookLM API")


@app.post("/generate_script")
def generate_and_save_script(
    pdf_path: str,
    filename: str = "response.json",
):
    """Generate a script from a PDF and save it to a JSON file."""

    if not pdf_path.endswith(".pdf"):
        raise ValueError("The provided path must be a PDF file.")

    script_obj = create_script_from_pdf(pdf_path)
    save_script_to_json(script_obj, filename)

    response_dict = {"response": script_obj.model_dump()}

    return response_dict


@app.get("/generate_audio")
def generate_audio(filename: str):
    """Generate audio files from a script saved in a JSON file."""
    if not filename.endswith(".json"):
        raise ValueError("The provided filename must be a JSON file.")

    with open(filename, "r") as f:
        response = json.load(f)

    if "response" not in response:
        raise ValueError("Response does not contain 'response' key.")

    output_filename = create_and_concatenate_audio(response["response"])
    return output_filename
