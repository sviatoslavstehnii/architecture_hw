import logging
import socket
import argparse
import os

from fastapi import FastAPI
from pydantic import BaseModel
import hazelcast
import consul
import uvicorn

import utils

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_hazelcast_config():
    c = consul.Consul()
    cluster_name = c.kv.get('hazelcast/logging/cluster_name')[1]['Value'].decode()
    members_raw = c.kv.get('hazelcast/logging/members')[1]['Value'].decode()
    members = members_raw.split(',')
    return cluster_name, members

cluster_name, cluster_members = get_hazelcast_config()


client = hazelcast.HazelcastClient(
    cluster_name=cluster_name,
    cluster_members=cluster_members,
)
message_store = client.get_map("message_store").blocking()

class LogMessage(BaseModel):
    uuid: str
    msg: str


@app.on_event("startup")
async def startup_event():
    port = int(os.getenv("APP_PORT", 8001))
    utils.register_service("logging-service", port)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/")
async def log_message(log: LogMessage):
    if log.msg in message_store.values():
        return {"status": "already exists", "data": {"message": "already exists"}}

    message_store.put(log.uuid, log.msg)
    logger.info(f"RECEIVED: {log}")
    return {"status": "ok", "data": {"uuid": log.uuid}}

@app.get("/")
async def get_logs():
    messages = list(message_store.values())
    logger.info(f"Logs requested")
    return {"status": "ok", "data": {"messages": ";".join(messages)}}

@app.on_event("shutdown")
def shutdown_event():
    client.shutdown()
    logger.info("Shutting down Hazelcast client")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8001, help="Port to run the logging-service on")
    args = parser.parse_args()

    os.environ["APP_PORT"] = str(args.port)
    uvicorn.run("logging_service:app", host="0.0.0.0", port=args.port, reload=False)
