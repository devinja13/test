import uvicorn
from src.api import app

from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True) #change this to host 0.0.0.0 when pushed to production