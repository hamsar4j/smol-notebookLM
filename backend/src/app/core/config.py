from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # llm api
    llm_base_url: str = os.getenv("LLM_BASE_URL", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
    llm_max_tokens: int = 500000

    # cartesia api
    cartesia_api_key: str = os.getenv("CARTESIA_API_KEY", "")
    cartesia_base_url: str = os.getenv("CARTESIA_BASE_URL", "")


settings = Settings()
