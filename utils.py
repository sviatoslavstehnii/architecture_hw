import socket
import consul


def register_service(service_name: str, port: int):
    c = consul.Consul()
    hostname = socket.gethostname()

    service_id = f"{service_name}-{hostname}-{port}"
    c.agent.service.register(
        name=service_name,
        service_id=service_id,
        address="localhost",
        port=port,
        check=consul.Check.http(f"http://localhost:{port}/health", interval="10s")
    )
    print(f"Registered {service_name} on port {port}")