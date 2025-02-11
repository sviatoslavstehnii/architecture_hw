import httpx


class MessageClient:
    
    def __init__(self, url="http://localhost:8002/"):
        self.MESSAGES_SERVICE_URL = url
    
    
    async def get_message(self):
        async with httpx.AsyncClient() as client:
            response_messages = await client.get(self.MESSAGES_SERVICE_URL)
            return response_messages.json()["data"]["message"]