"""
Conversation History Manager for AI CLI Assistant.
Handles in-memory context memory, system prompt configuration, and JSON file persistence.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class HistoryManager:
    def __init__(self, storage_path: Path, system_prompt: str = ""):
        self.storage_path = storage_path
        self.system_prompt = system_prompt
        self.messages: List[Dict[str, Any]] = []

    def set_system_prompt(self, prompt: str) -> None:
        """Sets or updates the system prompt."""
        self.system_prompt = prompt

    def add_user_message(self, content: str) -> None:
        """Appends a user message to the conversation history."""
        self.messages.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def add_assistant_message(self, content: str) -> None:
        """Appends an assistant message to the conversation history."""
        self.messages.append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def clear(self) -> None:
        """Clears all conversation messages, keeping the system prompt intact."""
        self.messages = []
        if self.storage_path.exists():
            try:
                self.storage_path.unlink()
            except Exception:
                pass

    def get_messages(self) -> List[Dict[str, Any]]:
        """Returns raw message history."""
        return self.messages

    def to_openai_format(self) -> List[Dict[str, str]]:
        """Formats context for OpenAI API calls."""
        formatted = []
        if self.system_prompt:
            formatted.append({"role": "system", "content": self.system_prompt})
        for msg in self.messages:
            formatted.append({"role": msg["role"], "content": msg["content"]})
        return formatted

    def to_gemini_format(self) -> List[Dict[str, Any]]:
        """Formats context for Google Gemini API calls."""
        formatted = []
        for msg in self.messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        return formatted

    def save(self) -> bool:
        """Persists system prompt and conversation messages to JSON file."""
        try:
            data = {
                "system_prompt": self.system_prompt,
                "updated_at": datetime.now().isoformat(),
                "messages": self.messages
            }
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving history: {e}")
            return False

    def load(self) -> bool:
        """Loads system prompt and conversation messages from JSON file if available."""
        if not self.storage_path.exists():
            return False
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.system_prompt = data.get("system_prompt", self.system_prompt)
            self.messages = data.get("messages", [])
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
            return False
