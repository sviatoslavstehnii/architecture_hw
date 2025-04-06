import httpx
import random
from tenacity import retry, stop_after_attempt, wait_fixed


class LoggingClient:
    def __init__(self, config_server_url="http://localhost:8006/services/logging-service"):
        self.config_server_url = config_server_url
        self.instances = []

    async def fetch_service_instances(self):
        """Fetch available logging-service instances from the config server."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.config_server_url)
                if response.status_code == 200:
                    self.instances = response.json().get("instances", [])
            except httpx.RequestError:
                pass

    def get_random_instance(self):
        """Return a random logging-service instance."""
        if not self.instances:
            raise ValueError("No available instances of logging-service")
        return random.choice(self.instances)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def create_message(self, payload):
        """Send a message to a random logging-service instance."""
        await self.fetch_service_instances()
        instance_url = self.get_random_instance()
        async with httpx.AsyncClient() as client:
            response = await client.post(instance_url, json=payload)
            return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def get_messages(self):
        """Retrieve messages from a random logging-service instance."""
        await self.fetch_service_instances()
        instance_url = self.get_random_instance()
        async with httpx.AsyncClient() as client:
            response = await client.get(instance_url)
            return response.json()["data"]["messages"]
