from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # llm api
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_api_key: str = os.getenv("GROQ_API_KEY", "")
    llm_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"


settings = Settings()
