from fastapi import FastAPI
from utils.get_text import get_PDF_text
from llm.router import generate_script
from llm.prompts import SYSTEM_PROMPT
from models.models import Transcript

app = FastAPI()


@app.get("/generate_script")
def get_script(system_prompt: str, input_text: str):
    text = get_PDF_text(input_text)
    response = generate_script(system_prompt, text, Transcript)
    return {"response": response}


print(get_script(system_prompt=SYSTEM_PROMPT, input_text="MoA.pdf"))
