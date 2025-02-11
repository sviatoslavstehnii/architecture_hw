import uuid
from fastapi import FastAPI

from clients.logging_client import LoggingClient
from clients.message_client import MessageClient

app = FastAPI()

logging_client = LoggingClient()
message_client = MessageClient()

@app.post("/")
async def create_message(msg: str):
    message_id = str(uuid.uuid4())
    payload = {"uuid": message_id, "msg": msg}

    response = await logging_client.create_message(payload)
    if response.json()["status"] == "already exists":
        return {"status": "message already exists"}

    return {"status": "message created"}


@app.get('/')
async def get_messages():

    messages = await logging_client.get_messages()
    message = await message_client.get_message()
    return {"status":"ok", "messages": messages + ";" + message}
