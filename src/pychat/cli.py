import os
import sys
from .chat_app import ChatApp

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    app = ChatApp()
    
    if app.session.messages:
        print(f"Resuming session: {app.session.session_id}")
    else:
        print(f"Started new session: {app.session.session_id}")

    print("Type 'new' to start a new session. Press Ctrl+C to exit.")

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue

            if user_input.lower() == "new":
                clear_screen()
                app.new_session()
                print(f"Started new session: {app.session.session_id}")
                continue

            print("AI: ", end="", flush=True)
            
            for content in app.send_message(user_input):
                print(content, end="", flush=True)
            
            print() # Newline after stream

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()

