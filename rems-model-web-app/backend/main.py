import os
import uvicorn
from src.api import app

from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True) #change this to host 0.0.0.0 when pushed to production
    