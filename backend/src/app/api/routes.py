import os
from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import FileResponse
from app.services.services import (
    create_script_from_pdf,
    build_audio_from_script,
)
from app.core.constants import PDF_DIR, MAX_FILE_SIZE, AUDIO_DIR
from app.models.models import AudioRequest
from werkzeug.utils import secure_filename

router = APIRouter()


@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)) -> dict:
    """Upload a PDF file and save it to the server."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="The uploaded file must be a PDF.")

    if file.size is None:
        raise HTTPException(status_code=400, detail="Could not determine file size.")

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    safe_filename = secure_filename(file.filename)
    file_location = os.path.join(PDF_DIR, safe_filename)

    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    return {"filename": file_location}


@router.post("/generate-audio")
def generate_audio(request: AudioRequest) -> FileResponse:
    """Generate audio files from a script saved in a JSON file."""
    pdf_name = secure_filename(request.filename)

    if not pdf_name:
        raise HTTPException(status_code=400, detail="Filename not provided.")

    pdf_path = os.path.join(PDF_DIR, os.path.basename(pdf_name))

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404, detail=f"PDF file not found at: {pdf_path}"
        )

    script_obj = create_script_from_pdf(pdf_path)
    script_dict = script_obj.model_dump()
    output_filename = build_audio_from_script(script_dict)

    if not os.path.exists(output_filename):
        raise HTTPException(status_code=500, detail="Audio file could not be created.")

    return FileResponse(
        output_filename,
        media_type="audio/wav",
        filename=os.path.basename(output_filename),
    )


@router.get("/get-audio")
def get_audio(filename: str) -> FileResponse:
    """Retrieve the audio file generated from the script."""
    if not filename.endswith(".wav"):
        raise HTTPException(
            status_code=400, detail="The provided filename must be a WAV file."
        )

    file_name = secure_filename(os.path.basename(filename))
    file_path = os.path.join(AUDIO_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found.")

    return FileResponse(file_path, media_type="audio/wav", filename=file_name)
