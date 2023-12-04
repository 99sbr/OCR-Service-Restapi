import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.initializer import IncludeAPIRouter

# Load environment variables from .env file
load_dotenv()


def get_application():
    """
    Creates FastAPI Object.
    """
    _app = FastAPI(title=os.environ['API_NAME'],
                   description=os.environ['API_DESCRIPTION'],
                   version=os.environ['API_VERSION'])
    _app.include_router(IncludeAPIRouter())
    _app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()
