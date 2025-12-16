from fastapi.testclient import TestClient
from backend.assistant.api import app

client = TestClient(app)

def test_chat_endpoint_validation():
    """Test that /chat rejects empty requests"""
    # Sending empty JSON
    response = client.post("/chat", json={}) 
    assert response.status_code == 422  # see if we get the error for empty message

def test_chat_endpoint_valid_structure():
    """Test that /chat accepts a valid response"""
    response = {
        "message": "Hello",
        "thread_id": "test_thread_123"
    }
    # Using stream=True to avoid waiting for the full generation
    with client.stream("POST", "/chat", json=response) as response:
        assert response.status_code == 200