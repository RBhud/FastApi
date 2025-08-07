from fastapi.testclient import TestClient

from .main import app, uploaded_file

# Create the test client
client = TestClient(app)

# test valid file uploads
def test_upload():
    
    # temporarily hold the uploaded file name if server is running
    temp = uploaded_file.filename

    # upload new csv file
    response = client.post(
        "/upload",
        files={"file": ("sample.csv", "sample data", "text/csv")},
    )
    
    assert response.status_code == 200
    assert response.json() == {"msg": "File Uploaded."}

    # reassign the file name
    uploaded_file.filename = temp

# test invalid file uploads
def test_invalid_upload():

    # upload invalid text file 
    response = client.post(
        "/upload",
        files={"file": ("sample.txt", "sample text", "text/plain")},
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Only CSV files are accepted."}

    # upload file with invalid content type
    response = client.post(
        "/upload",
        files={"file": ("sample.csv", "sample text", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Only 'text/csv' files are accepted."}

# test no file uploaded
def test_no_file():

    # temporarily set the uploaded file name to None
    temp = uploaded_file.filename
    uploaded_file.filename = None

    response = client.get("/summary/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "No files uploaded."}

    # reassign the file name
    uploaded_file.filename = temp
    

# test invalid user id
def test_invalid_user_id():

    # temporarily set the uploaded file name to dummy transactions
    temp = uploaded_file.filename
    uploaded_file.filename = "dummy_transactions.csv"

    response = client.get("/summary/1001")

    assert response.status_code == 404
    assert response.json() == {"detail" : "No records found for user id 1001"}

    # reassign the file name
    uploaded_file.filename = temp

# test valid user id
def test_valid_user_id():

    # temporarily set the uploaded file name to dummy transactions
    temp = uploaded_file.filename
    uploaded_file.filename = "dummy_transactions.csv"

    response = client.get("/summary/289")

    assert response.status_code == 200
    assert response.json() == {
                            "min": "5.12",
                            "max": "498.48",
                            "mean": "243.16170731707314"
                            }

    # reassign the file name
    uploaded_file.filename = temp
