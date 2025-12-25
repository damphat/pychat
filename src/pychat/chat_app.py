import os
from typing import List, Any
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from .chat_config import ChatConfig
from .data_session import Session, SESSIONS_DIR

class ChatApp:
    def __init__(self):
        self.client = OpenAI()
        self.config = ChatConfig.load()
        self.session = self._initialize_session()

    def _initialize_session(self) -> Session:
        """Initializes the session from config or creates a new one."""
        if self.config.last_session_id:
            session = Session.load(self.config.last_session_id)
            # Verify if session actually exists or has messages
            session_path = os.path.join(SESSIONS_DIR, f"chat-{self.config.last_session_id}.json")
            if not session.messages and not os.path.exists(session_path):
                return self.new_session()
            return session
        else:
            return self.new_session()

    def new_session(self) -> Session:
        """Starts a new session and updates config."""
        self.session = Session.create_new()
        self.config.last_session_id = self.session.session_id
        self.config.save()
        self.session.save()
        return self.session

    def send_message(self, user_input: str):
        """
        Sends a message to the AI and yields chunks of the response.
        Updates session history automatically.
        """
        # Append user message
        self.session.add_message("user", user_input)
        self.session.save()

        # Prepare messages for API
        api_messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.config.system}
        ]
        for msg in self.session.messages:
            api_messages.append(msg)  # type: ignore

        stream = self.client.chat.completions.create(
            model=self.config.model,
            messages=api_messages,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content
        
        # Append assistant response and save
        self.session.add_message("assistant", full_response)
        self.session.save()

    def set_model(self, name: str):
        """Set the model to `name` if OpenAI supports it, otherwise raise ValueError.

        This method queries the OpenAI models list and accepts model entries that are
        dicts with an 'id' key or objects with an 'id' attribute.
        """
        # Fetch list of models from OpenAI
        models_resp = self.client.models.list()
        # models_resp may be an iterable or have a .data attribute
        models_iter = getattr(models_resp, 'data', models_resp)

        supported = set()
        for m in models_iter:
            if isinstance(m, dict):
                mid = m.get('id')
            else:
                mid = getattr(m, 'id', None) or getattr(m, 'model', None)
            if mid:
                supported.add(mid)

        if name not in supported:
            raise ValueError(f"Model '{name}' is not supported by OpenAI.")

        # Persist the model in config
        self.config.model = name
        self.config.save()

    @property
    def messages(self):
        return self.session.messages
