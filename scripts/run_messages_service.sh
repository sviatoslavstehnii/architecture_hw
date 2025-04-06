hz-start --config=hazelcast/hazelcast-messaging.xml --port=5801 &
hz-start --config=hazelcast/hazelcast-messaging.xml --port=5802 &
uvicorn messages_service:app --host 0.0.0.0 --port 8004 &
uvicorn messages_service:app --host 0.0.0.0 --port 8005