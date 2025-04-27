import httpx
import random
from tenacity import retry, stop_after_attempt, wait_fixed


class LoggingClient:
    def __init__(self, consul_url="http://localhost:8500", service_name="logging-service"):
        self.consul_url = consul_url
        self.service_name = service_name
        self.instances = []

    async def fetch_service_instances(self):
        """Fetch available logging-service instances from Consul."""
        async with httpx.AsyncClient() as client:
            try:
                consul_service_url = f"{self.consul_url}/v1/health/service/{self.service_name}?passing"
                response = await client.get(consul_service_url)
                if response.status_code == 200:
                    services = response.json()
                    self.instances = []
                    for service in services:
                        service_info = service["Service"]
                        address = service_info["Address"]
                        port = service_info["Port"]
                        self.instances.append(f"http://{address}:{port}")
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
