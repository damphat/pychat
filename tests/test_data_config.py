import os
import json
import pytest
from chat_config import ChatConfig

TEST_CONFIG_PATH = "data/test_config.json"

@pytest.fixture
def cleanup():
    """Remove test config file if it exists."""
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)
    yield
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)

def test_config_default(cleanup):
    """Test that default config is used when file doesn't exist."""
    config = ChatConfig.load(TEST_CONFIG_PATH)
    assert config.system == "You are a helpful assistant."
    assert config.model == "gpt-5-nano"
    assert config.last_session_id is None

def test_config_save_load(cleanup):
    """Test saving and loading config."""
    config = ChatConfig(system="Custom System", model="custom-model", last_session_id="123")
    config.save(TEST_CONFIG_PATH)
    
    loaded_config = ChatConfig.load(TEST_CONFIG_PATH)
    assert loaded_config.system == "Custom System"
    assert loaded_config.model == "custom-model"
    assert loaded_config.last_session_id == "123"

def test_config_update(cleanup):
    """Test updating properties and saving."""
    config = ChatConfig.load(TEST_CONFIG_PATH)
    config.model = "new-model"
    config.save(TEST_CONFIG_PATH)
    
    loaded = ChatConfig.load(TEST_CONFIG_PATH)
    assert loaded.model == "new-model"

def test_config_corrupted_json(cleanup):
    """Test handling of invalid JSON files."""
    os.makedirs(os.path.dirname(TEST_CONFIG_PATH), exist_ok=True)
    with open(TEST_CONFIG_PATH, "w") as f:
        f.write("{ invalid json")
    
    config = ChatConfig.load(TEST_CONFIG_PATH)
    assert config.model == "gpt-5-nano" # Should fall back to default

def test_extra_fields(cleanup):
    """Test that extra fields in JSON are ignored."""
    os.makedirs(os.path.dirname(TEST_CONFIG_PATH), exist_ok=True)
    with open(TEST_CONFIG_PATH, "w") as f:
        json.dump({"model": "extra-model", "unknown_field": "ignore me"}, f)
    
    config = ChatConfig.load(TEST_CONFIG_PATH)
    assert config.model == "extra-model"
    assert not hasattr(config, "unknown_field")
