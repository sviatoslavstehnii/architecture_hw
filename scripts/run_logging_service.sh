hz-start --config=hazelcast/hazelcast-logging.xml --port=5701 &
hz-start --config=hazelcast/hazelcast-logging.xml --port=5702 &
hz-start --config=hazelcast/hazelcast-logging.xml --port=5703 &
python3 logging_service.py -p 8001 &
python3 logging_service.py -p 8002 &
python3 logging_service.py -p 8003