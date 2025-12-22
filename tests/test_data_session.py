import os
import json
import pytest
from data_session import Session

TEST_SESSIONS_DIR = "data/test_sessions"

@pytest.fixture
def cleanup():
    """Remove test sessions directory if it exists."""
    if os.path.exists(TEST_SESSIONS_DIR):
        import shutil
        shutil.rmtree(TEST_SESSIONS_DIR)
    yield
    if os.path.exists(TEST_SESSIONS_DIR):
        import shutil
        shutil.rmtree(TEST_SESSIONS_DIR)

def test_session_create_new():
    """Test creating a new session with UUID."""
    session = Session.create_new()
    assert session.session_id is not None
    assert len(session.session_id) > 0
    assert session.messages == []

def test_session_new():
    """Test creating a session with a specific ID."""
    session_id = "test-123"
    session = Session(session_id=session_id)
    assert session.session_id == session_id
    assert session.messages == []

def test_session_add_message():
    """Test adding messages to a session."""
    session = Session(session_id="test-123")
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi there!")
    
    assert len(session.messages) == 2
    assert session.messages[0] == {"role": "user", "content": "Hello"}
    assert session.messages[1] == {"role": "assistant", "content": "Hi there!"}

def test_session_save_load(cleanup):
    """Test saving and loading a session."""
    session_id = "test-save-load"
    session = Session(session_id=session_id)
    session.add_message("user", "Save this")
    session.save(sessions_dir=TEST_SESSIONS_DIR)
    
    # Check if file exists
    expected_path = os.path.join(TEST_SESSIONS_DIR, f"chat-{session_id}.json")
    assert os.path.exists(expected_path)
    
    # Load and verify
    loaded = Session.load(session_id, sessions_dir=TEST_SESSIONS_DIR)
    assert loaded.session_id == session_id
    assert len(loaded.messages) == 1
    assert loaded.messages[0]["content"] == "Save this"

def test_session_load_nonexistent():
    """Test loading a session that doesn't exist."""
    session = Session.load("nonexistent", sessions_dir=TEST_SESSIONS_DIR)
    assert session.session_id == "nonexistent"
    assert session.messages == []

def test_session_corrupted_json(cleanup):
    """Test handling of invalid session files."""
    session_id = "corrupted"
    os.makedirs(TEST_SESSIONS_DIR, exist_ok=True)
    path = os.path.join(TEST_SESSIONS_DIR, f"chat-{session_id}.json")
    with open(path, "w") as f:
        f.write("[ invalid json")
    
    session = Session.load(session_id, sessions_dir=TEST_SESSIONS_DIR)
    assert session.messages == []
