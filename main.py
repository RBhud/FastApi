from fastapi import FastAPI, File, UploadFile, HTTPException
from datetime import datetime
import csv
import os

class Filename:
    def __init__(self):
        self.filename = None

app = FastAPI()
# store the most recent uploaded filename
uploaded_file = Filename()

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

    # update the uploaded file ready for processing
    uploaded_file.filename = file.filename

    # store the file in the current directory
    with open(file_location, 'wb') as f:
        f.write(content)

    return {'msg' : "File Uploaded."}

# localhost:8000/summary/<user_id> endpoint
# get the summary of the user with the requested id 
@app.get("/summary/{user_id}")
async def get_summary(user_id: int):
    
    # check a file has been uploaded
    if uploaded_file.filename is None:
        raise HTTPException(status_code=404, detail="No files uploaded.")

    # initialise values for loop
    minimum = 1000000
    maximum = 0
    total_transaction_amount = 0
    record_count = 0
    minimum_date = ""
    maximum_date = ""

    # open the most recently uploaded file
    with open(uploaded_file.filename) as file:

        # read the csv file into lists of dictionaries
        reader = csv.DictReader(file)

        transaction_amount = 0
        # loop through all records belonging to the requested user
        for row in reader:

            if int(row.get("user_id")) == user_id:

                # get the minimum and maximum transaction amount
                transaction_amount = float(row.get("transaction_amount"))
                minimum = check_min(minimum, transaction_amount)
                maximum = check_max(maximum, transaction_amount)
                total_transaction_amount += transaction_amount
                record_count += 1

        # check if records are found for the user id
        if record_count == 0:
            raise HTTPException(status_code=404, detail=f"No records found for user id {user_id}")
        
        # calculate mean of all the users' transactions
        mean = total_transaction_amount / record_count

    return {"min": f"{minimum}", "max": f"{maximum}", "mean": f"{mean}"}

# check for minimum transaction amount
def check_min(current, check_val):
    if current < check_val:
        return current
    else:
        return check_val

# check for maximum transaction amount
def check_max(current, check_val):
    if current > check_val:
        return current
    else:
        return check_val
   