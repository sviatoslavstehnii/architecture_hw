import uuid
import socket
import argparse
import os

from fastapi import FastAPI
import hazelcast
import consul
import uvicorn

from clients.logging_client import LoggingClient
from clients.message_client import MessageClient
import utils

app = FastAPI()

logging_client = LoggingClient()
message_client = MessageClient()

client = hazelcast.HazelcastClient(
    cluster_name="messaging-cluster",
    cluster_members=[
        "127.0.0.1:5801",
        "127.0.0.1:5802",
    ],
)
queue = client.get_queue("messages-queue").blocking()


@app.on_event("startup")
async def startup_event():
    port = int(os.getenv("APP_PORT", 8000))
    utils.register_service("facade-service", port)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/")
async def create_message(msg: str):
    message_id = str(uuid.uuid4())
    payload = {"uuid": message_id, "msg": msg}
    queue.offer(msg)

    response = await logging_client.create_message(payload)
    if response.json()["status"] == "already exists":
        return {"status": "message already exists"}

    return {"status": "message created"}

@app.get("/")
async def get_messages():
    messages_logging = await logging_client.get_messages()
    messages_queue = await message_client.get_message()
    return {"status": "ok", "logging_service_messages": messages_logging,
            "messages_service_messages": ";".join(messages_queue)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run the facade-service on")
    args = parser.parse_args()

    os.environ["APP_PORT"] = str(args.port)
    uvicorn.run("facade_service:app", host="0.0.0.0", port=args.port, reload=False)
