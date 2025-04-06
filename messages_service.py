import threading
from fastapi import FastAPI
from hazelcast import HazelcastClient

app = FastAPI()

storage: list[str] = []

def consumer_loop():
    client = HazelcastClient(
        cluster_name="messaging-cluster",
        cluster_members=[
            "127.0.0.1:5801",
            "127.0.0.1:5802",
        ],
    )
    queue = client.get_queue("messages-queue").blocking()
    while True:
        item = queue.take()   
        storage.append(item)

threading.Thread(target=consumer_loop, daemon=True).start()

@app.get("/")
def get_messages():
    return {"status": "ok", "data": {"messages": storage}}
