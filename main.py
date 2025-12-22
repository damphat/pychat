import os
from openai import OpenAI
from chat_config import ChatConfig
from data_session import Session

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_new_session(config: ChatConfig) -> Session:
    """Creates a new Session and updates config."""
    clear_screen()
    session = Session.create_new()
    config.last_session_id = session.session_id
    config.save()
    session.save()
    print(f"Started new session: {session.session_id}")
    return session

def main():
    client = OpenAI()
    config = ChatConfig.load()
    
    # Initialize session
    session: Session
    if config.last_session_id:
        session = Session.load(config.last_session_id)
        if not session.messages and not os.path.exists(os.path.join("data", "sessions", f"chat-{config.last_session_id}.json")):
            # invalid session id or file missing, treat as new
            session = create_new_session(config)
        else:
            print(f"Resuming session: {session.session_id}")
    else:
        session = create_new_session(config)

    print("Type 'new' to start a new session. Press Ctrl+C to exit.")

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue

            if user_input.lower() == "new":
                session = create_new_session(config)
                continue

            # Append user message
            session.add_message("user", user_input)
            session.save()

            # Prepare messages for API
            api_messages = [{"role": "system", "content": config.system}] + session.messages

            print("AI: ", end="", flush=True)
            
            full_response = ""
            stream = client.chat.completions.create(
                model=config.model,
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
            session.add_message("assistant", full_response)
            session.save()

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()

