import random
import socket
import json
import time
from confluent_kafka import Producer

conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": socket.gethostname(),
}
producer = Producer(conf)
TOPIC = "my-topic"
SLEEP_TIME = 1, 5


def get_message() -> dict:
    return {
        "value": f"{random.random()}",
    }


def start_produce(producer, topic):
    try:
        while True:
            key = "sensor-1"
            time.sleep(random.randint(*SLEEP_TIME))
            value = json.dumps(get_message())
            producer.produce(topic, key=key, value=value)
            producer.flush()

    except KeyboardInterrupt:
        pass

    finally:
        producer.flush()
        producer.close()


start_produce(producer, topic=TOPIC)

# @app.post("/produce")
# async def produce(key: str):
# producer.produce("my-topic", key="key", value=key)
# return {"status": "success"}
