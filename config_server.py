from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI()

CONFIG_FILE = os.getenv("CONFIG_FILE", "cfg.json")

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

config_data = load_config()

@app.get("/services/{service_name}")
async def get_service_ips(service_name: str):
    if service_name in config_data:
        return {"service": service_name, "instances": config_data[service_name]}
    raise HTTPException(status_code=404, detail="Service not found")

