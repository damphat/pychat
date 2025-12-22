import os
import json
import uuid
from openai import OpenAI
from typing import List, Dict, Any, Optional

# Constants
DATA_DIR = "data"
SESSIONS_DIR = os.path.join(DATA_DIR, "sessions")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def load_config() -> Dict[str, Any]:
    """Loads the configuration file."""
    default_config = {
        "system": "You are a helpful assistant.",
        "model": "gpt-4o",
        "last_session_id": None
    }
    if not os.path.exists(CONFIG_FILE):
        return default_config
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
        # Ensure default keys exist
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
        return config

def save_config(config: Dict[str, Any]):
    """Saves the configuration file."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def get_session_file(session_id: str) -> str:
    return os.path.join(SESSIONS_DIR, f"chat-{session_id}.json")

def load_session(session_id: str) -> List[Dict[str, str]]:
    """Loads chat history for a given session ID."""
    session_file = get_session_file(session_id)
    if os.path.exists(session_file):
        with open(session_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_session(session_id: str, messages: List[Dict[str, str]]):
    """Saves chat history for a session."""
    session_file = get_session_file(session_id)
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_new_session(config: Dict[str, Any]) -> tuple[str, List[Dict[str, str]]]:
    """Creates a new session ID and updates config."""
    clear_screen()
    session_id = str(uuid.uuid4())
    config["last_session_id"] = session_id
    save_config(config)
    save_session(session_id, [])
    print(f"Started new session: {session_id}")
    return session_id, []

def main():
    # Ensure data directories exist
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    client = OpenAI()
    config = load_config()
    system_prompt = config.get("system", "You are a helpful assistant.")
    
    current_session_id = config.get("last_session_id")
    
    # Initialize session
    messages: List[Dict[str, str]] = []
    if current_session_id:
        messages = load_session(current_session_id)
        if not messages and not os.path.exists(get_session_file(current_session_id)):
             # invalid session id or file missing, treat as new
             pass
        else:
            print(f"Resuming session: {current_session_id}")
    
    if not current_session_id or (current_session_id and not messages and not os.path.exists(get_session_file(current_session_id))):
        current_session_id, messages = create_new_session(config)

    print("Type 'new' to start a new session. Press Ctrl+C to exit.")

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue

            if user_input.lower() == "new":
                current_session_id, messages = create_new_session(config)
                continue

            # Append user message
            messages.append({"role": "user", "content": user_input})
            save_session(current_session_id, messages)

            # Prepare messages for API (include system prompt if not present in history, 
            # though actually usually system prompt is separate or header)
            # The requirement says "gửi kèm system prompt và chat history của session hiện tại"
            
            api_messages = [{"role": "system", "content": system_prompt}] + messages

            print("AI: ", end="", flush=True)
            
            full_response = ""
            stream = client.chat.completions.create(
                model=config.get("model", "gpt-4o"),
                messages=api_messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print() # Newline after stream

            # Append assistant response
            messages.append({"role": "assistant", "content": full_response})
            save_session(current_session_id, messages)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
