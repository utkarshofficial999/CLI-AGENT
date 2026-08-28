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
        self.system_prompt = prompt

    def add_user_message(self, content: str) -> None:
        self.messages.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def clear(self) -> None:
        self.messages = []
        if self.storage_path.exists():
            try:
                self.storage_path.unlink()
            except Exception:
                pass

    def get_messages(self) -> List[Dict[str, Any]]:
        return self.messages

    def to_openai_format(self) -> List[Dict[str, str]]:
        formatted = []
        if self.system_prompt:
            formatted.append({"role": "system", "content": self.system_prompt})
        for msg in self.messages:
            formatted.append({"role": msg["role"], "content": msg["content"]})
        return formatted

    def to_gemini_format(self) -> List[Dict[str, Any]]:
        formatted = []
        for msg in self.messages:
            role = "user" if msg["role"] == "user" else "model"
            formatted.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        return formatted

    def save(self) -> bool:
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
