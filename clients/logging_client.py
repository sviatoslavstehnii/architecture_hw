import httpx
from tenacity import retry, stop_after_attempt, wait_fixed



class LoggingClient:
    
    def __init__(self, url="http://localhost:8001/"):
        self.LOGGING_SERVICE_URL = url
    
    @retry(stop=stop_after_attempt(2), wait=wait_fixed(5))
    async def create_message(self, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.LOGGING_SERVICE_URL, json=payload)
            return response
    
    @retry(stop=stop_after_attempt(2), wait=wait_fixed(5))
    async def get_messages(self):
        async with httpx.AsyncClient() as client:
            response_logging = await client.get(self.LOGGING_SERVICE_URL)
            return response_logging.json()["data"]["messages"]
        