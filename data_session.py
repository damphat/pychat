from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json
import os
import uuid

DATA_DIR = "data"
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")

@dataclass
class Session:
    session_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def create_new(cls) -> 'Session':
        """Create a new session with a unique UUID."""
        return cls(session_id=str(uuid.uuid4()))

    @classmethod
    def load(cls, session_id: str, sessions_dir: str = SESSIONS_DIR) -> 'Session':
        """Load a session by its ID from a specific directory. Returns a new session if not found."""
        path = os.path.join(sessions_dir, f"chat-{session_id}.json")
        if not os.path.exists(path):
            return cls(session_id=session_id)
        try:
            with open(path, "r", encoding="utf-8") as f:
                messages = json.load(f)
                if not isinstance(messages, list):
                    messages = []
                return cls(session_id=session_id, messages=messages)
        except (json.JSONDecodeError, OSError):
            return cls(session_id=session_id)

    def save(self, sessions_dir: str = SESSIONS_DIR):
        """Save the current session to a JSON file in the specified directory."""
        os.makedirs(sessions_dir, exist_ok=True)
        path = os.path.join(sessions_dir, f"chat-{self.session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=4, ensure_ascii=False)

    def add_message(self, role: str, content: str):
        """Add a message to the session."""
        self.messages.append({"role": role, "content": content})
