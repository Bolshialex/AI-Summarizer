@echo off
echo Starting FastAPI server on Windows...

:: Activate the virtual environment
call venv\Scripts\activate

:: Install and update dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt

:: Run the server
echo Starting the server...
uvicorn main:app --reload