import httpx
import random

class MessageClient:
    def __init__(
        self,
        config_server_url: str = "http://localhost:8006/services/messages-service",
    ):
        self.config_server_url = config_server_url
        self.instances: list[str] = []

    async def fetch_service_instances(self) -> None:
        """Fetch available messages‑service instances from the config server."""
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(self.config_server_url)
                resp.raise_for_status()
                self.instances = resp.json().get("instances", [])
            except (httpx.RequestError, httpx.HTTPStatusError):
                self.instances = []

    def get_random_instance(self) -> str:
        """Return a random messages‑service instance URL."""
        if not self.instances:
            raise ValueError("No available instances of messages‑service")
        return random.choice(self.instances)

    async def get_message(self) -> str:
        """Retrieve a single message from a random messages‑service instance."""
        await self.fetch_service_instances()
        instance_url = self.get_random_instance()
        async with httpx.AsyncClient() as client:
            resp = await client.get(instance_url)
            resp.raise_for_status()
            return resp.json()["data"]["messages"]
