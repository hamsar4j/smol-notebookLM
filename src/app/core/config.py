from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    # llm api
    llm_base_url: str = os.getenv("LLM_BASE_URL", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = "meta-llama/Llama-4-Scout-17B-16E-Instruct"


settings = Settings()
