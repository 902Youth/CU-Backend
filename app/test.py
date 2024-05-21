import pytest
from app import app

@pytest.fixture
def client():
    # Create a test client using the Flask application context
    with app.test_client() as client:
        yield client

def test_welcome(client):
    # Send a GET request to the root URL
    response = client.get('/')
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    # Check if the response data contains the expected message
    assert b"Welcome to the API!" in response.data
