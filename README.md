The first steps I took when approaching this challenge was understanding the requirements and breaking them down into smaller parts.
For example, the first endpoint /upload was broken into three steps: Upload CSV, Validate and Store.
Before implementing the endpoint I wrote some unit tests that determined what code I would write to allow that test to pass.
This allowed me to ensure my code is error and bug free.
For the second endpoint '/summary/<user_id>' I repeated the same steps. I also thought about how an actual user, who does not know 
the code would act. If no file was uploaded, the user could not request any user data.

Setup intructions
In command prompt enter:
  - pip install fastapi
  - pip install uvicorn
    
To run tests
  - pip install pytest
  - enter: "pytest" in the command prompt in your working directory
  - for more information run "pytest -vv"

To run the server
  - enter: "fastapi dev main.py"

To test the endpoints
  - go to localhost:8000/docs and select try on the /upload endpoint to upload a CSV file from your device
  - you can then either use the UI to try the /summary/<user_id> endpoint or go to localhost:8000/summary/<user_id> where <user_id> is a number
    between 1-1000
