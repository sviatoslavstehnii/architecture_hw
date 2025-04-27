import os
import threading
import logging
import socket
import argparse

from fastapi import FastAPI
from hazelcast import HazelcastClient
import consul
import uvicorn

import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
storage: list[dict] = []

def get_queue_config_from_consul():
    c = consul.Consul()
    cluster_name = c.kv.get('messaging/queue/cluster_name')[1]['Value'].decode()
    members_raw = c.kv.get('messaging/queue/members')[1]['Value'].decode()
    queue_name = c.kv.get('messaging/queue/queue_name')[1]['Value'].decode()
    members = members_raw.split(',')
    return cluster_name, members, queue_name


@app.on_event("startup")
async def startup_event():
    port = int(os.getenv("APP_PORT", 8004))
    utils.register_service("messages-service", port)

def consumer_loop():
    cluster_name, cluster_members, queue_name = get_queue_config_from_consul()

    client = HazelcastClient(
        cluster_name=cluster_name,
        cluster_members=cluster_members,
    )
    queue = client.get_queue(queue_name).blocking()

    while True:
        item = queue.take()
        logger.info(f"RECEIVED: {item}")
        storage.append(item)

threading.Thread(target=consumer_loop, daemon=True).start()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
def get_messages():
    return {"status": "ok", "data": {"messages": storage}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8004, help="Port to run the messages-service on")
    args = parser.parse_args()

    os.environ["APP_PORT"] = str(args.port)
    uvicorn.run("messages_service:app", host="0.0.0.0", port=args.port, reload=False)
