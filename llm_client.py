"""
Unified LLM Client supporting Groq, Google Gemini, and OpenAI with real-time streaming.
"""

from abc import ABC, abstractmethod
from typing import Generator, Optional
import config
from history_manager import HistoryManager


class BaseLLMClient(ABC):
    """Abstract Base Class for LLM Client implementations."""

    @abstractmethod
    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        """Streams response tokens yield by yield from the active LLM provider."""
        pass


class GroqClient(BaseLLMClient):
    """Groq High-Speed LLM Provider Client using the official groq SDK."""

    def __init__(self, api_key: str, model_name: str = config.GROQ_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        try:
            from groq import Groq
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
    """Google Gemini LLM Provider Client using the official google-genai SDK."""

    def __init__(self, api_key: str, model_name: str = config.GEMINI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google GenAI Client: {e}")

    def stream_response(self, history: HistoryManager) -> Generator[str, None, None]:
        from google.genai import types

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
    """OpenAI LLM Provider Client using the official openai SDK."""

    def __init__(self, api_key: str, model_name: str = config.OPENAI_MODEL):
        self.api_key = api_key
        self.model_name = model_name
        try:
            from openai import OpenAI
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


def create_llm_client(provider: Optional[str] = None) -> BaseLLMClient:
    """
    Factory function to create an LLM client based on requested or auto-detected provider.
    """
    selected_provider = provider or config.get_active_provider()

    if selected_provider == "groq":
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
            "No valid API key found. Please set GROQ_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in your .env file."
        )
