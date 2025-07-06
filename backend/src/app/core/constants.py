import os

STORAGE_DIR = "storage"
PDF_DIR = os.path.join(STORAGE_DIR, "pdfs")
TEXT_DIR = os.path.join(STORAGE_DIR, "texts")
AUDIO_DIR = "audio_output"
MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
