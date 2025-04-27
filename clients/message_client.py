import httpx
import random

class MessageClient:
    def __init__(self, consul_url: str = "http://localhost:8500", service_name: str = "messages-service"):
        self.consul_url = consul_url
        self.service_name = service_name
        self.instances: list[str] = []

    async def fetch_service_instances(self) -> None:
        """Fetch available messages-service instances from Consul."""
        async with httpx.AsyncClient() as client:
            try:
                consul_service_url = f"{self.consul_url}/v1/health/service/{self.service_name}?passing"
                resp = await client.get(consul_service_url)
                resp.raise_for_status()
                services = resp.json()
                self.instances = []
                for service in services:
                    service_info = service["Service"]
                    address = service_info["Address"]
                    port = service_info["Port"]
                    self.instances.append(f"http://{address}:{port}")
            except (httpx.RequestError, httpx.HTTPStatusError):
                self.instances = []

    def get_random_instance(self) -> str:
        """Return a random messages-service instance URL."""
        if not self.instances:
            raise ValueError("No available instances of messages-service")
        return random.choice(self.instances)

    async def get_message(self) -> str:
        """Retrieve a single message from a random messages-service instance."""
        await self.fetch_service_instances()
        instance_url = self.get_random_instance()
        async with httpx.AsyncClient() as client:
            resp = await client.get(instance_url)
            resp.raise_for_status()
            return resp.json()["data"]["messages"]
