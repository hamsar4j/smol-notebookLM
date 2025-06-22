from pydantic import BaseModel
from typing import Literal, List

class LineItem(BaseModel):
    speaker: Literal["Host (Jane)", "Guest (John)"]
    text: str

class Transcript(BaseModel):
    scratchpad: str
    name_of_guest: str
    script: List[LineItem]