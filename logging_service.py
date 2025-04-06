from fastapi import FastAPI
from pydantic import BaseModel
import hazelcast
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = hazelcast.HazelcastClient(
    cluster_name="logging-cluster",
        cluster_members=[
            "127.0.0.1:5701",
            "127.0.0.1:5702",
            "127.0.0.1:5703",
        ],
)
message_store = client.get_map("message_store").blocking()

class LogMessage(BaseModel):
    uuid: str
    msg: str

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

