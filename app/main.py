import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
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


@app.post("/notifications")
async def notify():
    try:
        message_api_client.send_text_with_open_id(OPEN_ID, "hi")
        return {"code": 0, "message": "ok"}
    except HTTPError as e:
        return {"code": -1, "message": e.response.json()}
    except LarkException as e:
        return {"code": -1, "message": e}
