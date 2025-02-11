from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

message_store: Dict[str, str] = {}

class LogMessage(BaseModel):
    uuid: str
    msg: str

@app.post("/")
async def log_message(log: LogMessage):
    if log.msg in message_store.values():
        return {"status": "already exists", "data": {"message": "already exists"}}

    message_store[log.uuid] = log.msg
    print(f"RECEIVED: {log}")
    return {"status": "ok", "data": {"uuid": log.uuid}}

@app.get("/")
async def get_logs():
    return {"status": "ok", "data": {"messages": ";".join(message_store.values())}}
