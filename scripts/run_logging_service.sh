hz-start --config=hazelcast/hazelcast-logging.xml --port=5701 &
hz-start --config=hazelcast/hazelcast-logging.xml --port=5702 &
hz-start --config=hazelcast/hazelcast-logging.xml --port=5703 &
uvicorn logging_service:app --host 0.0.0.0 --port 8001 &
uvicorn logging_service:app --host 0.0.0.0 --port 8002 &
uvicorn logging_service:app --host 0.0.0.0 --port 8003