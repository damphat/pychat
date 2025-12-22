from typing import Optional
from dataclasses import dataclass, asdict
import json 
import os

DATA_DIR = "data"
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

@dataclass
class ChatConfig:
    system: str = "You are a helpful assistant."
    model: str = "gpt-5-nano"
    last_session_id: Optional[str] = None

    @classmethod
    def load(cls, path: str = CONFIG_FILE) -> 'ChatConfig':
        """Load config from path, or return default if not found."""
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Only use keys that exist in the dataclass to avoid errors on extra fields
                valid_keys = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
                return cls(**valid_keys)
        except (json.JSONDecodeError, OSError):
            return cls()

    def save(self, path: str = CONFIG_FILE):
        """Save current config to path."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)