import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")
    MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "1200"))
    ENABLE_AI = os.getenv("ENABLE_AI", "false").lower() == "true"

    DATA_PATH = os.getenv("DATA_PATH", "data/itsm_tickets_sample_v1.csv")
    REPORT_PATH = os.getenv("REPORT_PATH", "reports")

config = Config()