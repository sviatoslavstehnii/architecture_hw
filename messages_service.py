import threading
import logging
from fastapi import FastAPI
from hazelcast import HazelcastClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
storage: list[dict] = []

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
        item = queue.take()                # blocks until a message arrives
        logger.info(f"RECEIVED: {item}")   # now this will actually print
        storage.append(item)

threading.Thread(target=consumer_loop, daemon=True).start()

@app.get("/")
def get_messages():
    return {"status": "ok", "data": {"messages": storage}}
