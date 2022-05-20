import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from requests.exceptions import HTTPError

from .feishu import LarkException, MessageApiClient

# load env parameters from file named .env
load_dotenv(find_dotenv())

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
OPEN_ID = os.getenv("OPEN_ID")
LARK_HOST = os.getenv("LARK_HOST", 'https://open.feishu.cn')

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Notification(BaseModel):
    content: str


@app.post("/notifications")
async def notify(noti: Notification):
    message_api_client.send_text_with_open_id(OPEN_ID, noti.content)
    return {"code": 0, "message": "ok"}


@app.exception_handler(HTTPError)
async def http_exception_handler(request: Request, exc: HTTPError):
    return JSONResponse(
        status_code=500,
        content={"code": -1, "message": exc.response.json()},
    )


@app.exception_handler(LarkException)
async def lark_exception_handler(request: Request, exc: LarkException):
    return JSONResponse(
        status_code=500,
        content={"code": -1, "message": exc},
    )
