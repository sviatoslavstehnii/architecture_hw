from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_message():
    return {"status": "ok", "data": {"message": "not implemented yet"}}
