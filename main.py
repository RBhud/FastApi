from fastapi import FastAPI, File, UploadFile, HTTPException
import csv
import os

app = FastAPI()

# localhost:8000/upload endpoint
# Upload file to endpoint and check CSV validity
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    # check if the file is a .csv
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    # check if the media type is text/csv
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only 'text/csv' files are accepted.")

    # check file can be parsed as a csv
    try:
        content = await file.read()
        decoded_file = content.decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    # get the current directory to store the file in
    current_dir = os.getcwd()

    # build the path
    file_location = os.path.join(current_dir, file.filename)

    # store the file in the current directory
    with open(file_location, 'wb') as f:
        f.write(content)

    return {'msg' : "File Uploaded."}