hz-start --config=hazelcast/hazelcast-messaging.xml --port=5801 &
hz-start --config=hazelcast/hazelcast-messaging.xml --port=5802 &
python3 messages_service.py -p 8004 &
python3 messages_service.py -p 8005