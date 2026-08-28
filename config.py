import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "auto").strip().lower()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

DEFAULT_SYSTEM_PROMPT = os.getenv(
    "DEFAULT_SYSTEM_PROMPT",
    "You are a helpful, concise, and smart AI Assistant running inside a terminal CLI environment."
).strip()

HISTORY_FILE = BASE_DIR / ".chat_history.json"


def get_active_provider() -> str:
    if DEFAULT_PROVIDER in ("groq", "gemini", "openai"):
        return DEFAULT_PROVIDER

    if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
        return "groq"
    elif GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
        return "gemini"
    elif OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
        return "openai"

    return "none"
