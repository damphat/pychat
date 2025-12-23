import pytest
from unittest.mock import MagicMock, patch
from chat_app import ChatApp
from data_session import Session
from chat_config import ChatConfig

@pytest.fixture
def mock_openai():
    with patch('chat_app.OpenAI') as mock:
        yield mock

@pytest.fixture
def mock_config():
    with patch('chat_app.ChatConfig.load') as mock:
        mock.return_value = ChatConfig(last_session_id=None)
        yield mock

def test_chat_app_init(mock_openai, mock_config):
    app = ChatApp()
    assert app.client is not None
    assert app.config is not None
    assert app.session is not None
    assert isinstance(app.session, Session)

def test_chat_app_new_session(mock_openai, mock_config):
    app = ChatApp()
    old_id = app.session.session_id
    new_session = app.new_session()
    assert new_session.session_id != old_id
    assert app.session == new_session
    assert app.config.last_session_id == new_session.session_id

@patch('chat_app.Session.save')
def test_chat_app_send_message(mock_save, mock_openai, mock_config):
    app = ChatApp()
    
    # Mock the stream response
    mock_chunk = MagicMock()
    mock_chunk.choices = [MagicMock()]
    mock_chunk.choices[0].delta.content = "Hello"
    
    mock_stream = [mock_chunk]
    app.client.chat.completions.create.return_value = mock_stream
    
    responses = list(app.send_message("Hi"))
    
    assert responses == ["Hello"]
    assert len(app.session.messages) == 2
    assert app.session.messages[0] == {"role": "user", "content": "Hi"}
    assert app.session.messages[1] == {"role": "assistant", "content": "Hello"}
    assert app.client.chat.completions.create.called


def test_set_model_valid(mock_openai, mock_config):
    app = ChatApp()

    # Prepare models returned by OpenAI
    app.client.models.list.return_value = MagicMock(data=[{"id": "gpt-5-nano"}, {"id": "gpt-4"}])

    with patch.object(ChatConfig, 'save') as mock_save:
        app.set_model("gpt-4")
        assert app.config.model == "gpt-4"
        mock_save.assert_called_once()


def test_set_model_invalid(mock_openai, mock_config):
    app = ChatApp()
    app.client.models.list.return_value = MagicMock(data=[{"id": "gpt-5-nano"}])

    with pytest.raises(ValueError):
        app.set_model("gpt-4")
