import json
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.services.services import (
    create_script_from_pdf,
    save_script_to_json,
    create_and_concatenate_audio,
)
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="SMOL NotebookLM API")

origins = [
    "http://localhost:3000",  # The default port for Next.js
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STORAGE_DIR = "storage"
PDF_DIR = os.path.join(STORAGE_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)

@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)) -> dict:
    """Upload a PDF file and save it to the server."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="The uploaded file must be a PDF.")

    filename = file.filename
    file_location = os.path.join(PDF_DIR, filename)

    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    return {"filename": file_location}

@app.post("/generate-script")
def generate_script(
    pdf_path: str,
    filename: str = "response.json",
) -> dict:
    """Generate a script from a PDF and save it to a JSON file."""
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found.")

    script_obj = create_script_from_pdf(pdf_path)
    save_script_to_json(script_obj, filename)

    response_dict = {"response": script_obj.model_dump()}

    return response_dict


@app.post("/generate-audio")
def generate_audio(filename: str) -> str:
    """Generate audio files from a script saved in a JSON file."""
    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="The provided filename must be a JSON file.")
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="JSON file not found.")

    with open(filename, "r") as f:
        try:
            response = json.load(f)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON file.")

    if "response" not in response:
        raise HTTPException(status_code=400, detail="Response does not contain 'response' key.")

    output_filename = create_and_concatenate_audio(response["response"])

    # return FileResponse(output_filename, media_type="audio/wav", filename=os.path.basename(output_filename))
    return output_filename

@app.get("/get-script")
def get_script(filename: str) -> dict:
    """Retrieve the script from a JSON file."""
    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="The provided filename must be a JSON file.")
    
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="JSON file not found.")

    with open(filename, "r") as f:
        response = json.load(f)

    if "response" not in response:
        raise ValueError("Response does not contain 'response' key.")
    
    # return FileResponse(filename, media_type="application/json", filename=os.path.basename(filename))

    return response["response"]

@app.get("/get-audio")
def get_audio(filename: str) -> str:
    """Retrieve the audio file generated from the script."""
    if not filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="The provided filename must be a WAV file.")

    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return filename
    # return FileResponse(filename, media_type="audio/wav", filename=os.path.basename(filename))



# if __name__ == "__main__":

#     response_dict = generate_and_save_script(
#         pdf_path="MoA.pdf",
#         filename="response.json",
#     )
#     generate_audio(filename="response.json")
