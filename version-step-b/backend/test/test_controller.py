from starlette.testclient import TestClient
from starlette.responses import Response
from fileServer import app  # replace with your actual module and function names
import pytest

from utils.helper import delete_file

@pytest.fixture
def client():
    return TestClient(app)

def test_shakehands(client):
    response = client.get("/shakehands")
    
    # Check status code
    assert response.status_code == 200

    # Check JSON keys
    json = response.json()
    assert "public_key" in json

    # Check cookies
    cookies = response.cookies
    assert "session_id" in cookies
    assert "csrf_token" in cookies

def test_create_upload_file(client):
    # Call shakehands to get session_id and csrf_token
    shakehands_response = client.get("/shakehands")
    cookies = shakehands_response.cookies
    
    # Create a temporary test file
    test_file_path = "uploads/test/image.png"    

    # Make a request to the create_upload_file endpoint with cookies
    response = client.post("/upload", files={"file": open(test_file_path, "rb")}, cookies=cookies)

    # Assert that the response status code is 201 (created)
    assert response.status_code == 201

    # Assert that the file was uploaded successfully
    assert response.json()["message"] == "File uploaded successfully"

    # Clean up the test file
    delete_file(response.json()["filename"])    
    
