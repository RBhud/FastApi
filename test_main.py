from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_upload():

    response = client.post(
        "/upload",
        files={"file": ("sample.csv", "sample data", "text/csv")},
    )
    
    assert response.status_code == 200
    assert response.json() == {"msg": "File Uploaded."}

def test_invalid_upload():

    response = client.post(
        "/upload",
        files={"file": ("sample.txt", "sample text", "text/plain")},
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files are accepted."}

    response = client.post(
        "/upload",
        files={"file": ("sample.csv", "sample text", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Only 'text/csv' files are accepted."}
