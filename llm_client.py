from abc import ABC, abstractmethod
from typing import Generator, Optional
import config
from history_manager import HistoryManager

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class BaseLLMClient(ABC):

    @abstractmethod
    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        pass


class GroqClient(BaseLLMClient):

    def __init__(self, api_key: str, model_name: str = config.GROQ_MODEL):
        if Groq is None:
            raise RuntimeError("The 'groq' package is not installed. Please run: pip install groq")
        self.api_key = api_key
        self.model_name = model_name
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Groq Client: {e}")

    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        messages = history.to_openai_format()

        try:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True
            )
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[API Error (Groq)]: {e}"


class GeminiClient(BaseLLMClient):

    def __init__(self, api_key: str, model_name: str = config.GEMINI_MODEL):
        if genai is None:
            raise RuntimeError("The 'google-genai' package is not installed. Please run: pip install google-genai")
        self.api_key = api_key
        self.model_name = model_name
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google GenAI Client: {e}")

    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        contents = history.to_gemini_format()
        sys_instruction = history.system_prompt if history.system_prompt else None

        req_config = types.GenerateContentConfig(
            system_instruction=sys_instruction
        ) if sys_instruction else None

        try:
            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=req_config
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n[API Error (Gemini)]: {e}"


class OpenAIClient(BaseLLMClient):

    def __init__(self, api_key: str, model_name: str = config.OPENAI_MODEL):
        if OpenAI is None:
            raise RuntimeError("The 'openai' package is not installed. Please run: pip install openai")
        self.api_key = api_key
        self.model_name = model_name
        try:
            self.client = OpenAI(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI Client: {e}")

    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        messages = history.to_openai_format()

        try:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True
            )
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[API Error (OpenAI)]: {e}"


class OllamaClient(BaseLLMClient):

    def __init__(self, host: str = config.OLLAMA_HOST, model_name: str = config.OLLAMA_MODEL):
        if OpenAI is None:
            raise RuntimeError("The 'openai' package is not installed. Please run: pip install openai")
        self.host = host
        self.model_name = model_name
        base_url = f"{self.host.rstrip('/')}/v1"
        try:
            self.client = OpenAI(base_url=base_url, api_key="ollama")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Ollama Client: {e}")

    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        messages = history.to_openai_format()

        try:
            response_stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True
            )
            for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield (
                f"\n[Connection Error (Ollama)]: {e}\n"
                f"💡 Troubleshooting:\n"
                f"1. Make sure Ollama app is running locally on {self.host}\n"
                f"2. Ensure you downloaded the model: open a terminal and run `ollama pull {self.model_name}`\n"
            )


def create_llm_client(provider: Optional[str] = None) -> BaseLLMClient:
    selected_provider = provider or config.get_active_provider()

    if selected_provider == "ollama":
        return OllamaClient(host=config.OLLAMA_HOST, model_name=config.OLLAMA_MODEL)

    elif selected_provider == "groq":
        if not config.GROQ_API_KEY or config.GROQ_API_KEY == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set in your .env file. "
                "Please add your key to .env or set GROQ_API_KEY environment variable."
            )
        return GroqClient(api_key=config.GROQ_API_KEY)

    elif selected_provider == "gemini":
        if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "your_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY is not set in your .env file. "
                "Please add your key to .env or set GEMINI_API_KEY environment variable."
            )
        return GeminiClient(api_key=config.GEMINI_API_KEY)

    elif selected_provider == "openai":
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError(
                "OPENAI_API_KEY is not set in your .env file. "
                "Please add your key to .env or set OPENAI_API_KEY environment variable."
            )
        return OpenAIClient(api_key=config.OPENAI_API_KEY)

    else:
        raise ValueError(
            "No valid provider found. Please set DEFAULT_PROVIDER=ollama or configure API keys in your .env file."
        )

