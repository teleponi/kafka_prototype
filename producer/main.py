"""
Kafka Producer Beispiel

Ein Kafka Producer produziert fake Sensordaten und sendet sie 
via einem Topic in den Kafka-Cluster. 

Beispielhaft werden Temperaturdaten generiert, die auf einer Gauß-Verteilung
beruhen und mit einer Wahrscheinlichkeit von 10% einen NAN-Wert senden.
"""


import random
import socket
import json
import time
from datetime import datetime
from confluent_kafka import Producer


conf = {
    "bootstrap.servers": "kafka:9092",
    "client.id": socket.gethostname(),
}


def get_random_machine_temperature() -> float:
    """Random machine temperature in Celsius.

    Generate a random sample from a gaussian distribution.
    For the sake of a prototype, we use a fix mean temperature and deviation.

    In rare cases, sensors don't provide a numeric value. We simulate this
    with return a NAN-Value once in a while.

    Returns:
        Machine Temperature: float
    """
    mu = 30
    sigma = 2
    probability_nan = 0.1

    # in rare cases, sensors produce nan value
    if random.random() <= probability_nan:
        return float("nan")
    return random.gauss(mu=mu, sigma=sigma)


def get_message(topics) -> tuple[str, dict]:
    """Generate fake sensor message.

    Returns:
        a tuple of topic and data
    """
    topic = random.choice(topics)
    data = {
        "sensor": topic,
        "temp": get_random_machine_temperature(),
        "time": datetime.now().strftime("%d%m%Y: %H:%M"),
    }

    return topic, data


def start_produce(producer: Producer) -> None:
    """Main Producer Loop."""
    try:
        while True:
            time.sleep(random.randint(*SLEEP_TIME))
            topic, data = get_message(TOPICS)
            value = json.dumps(data)
            producer.produce(topic, value=value)  # key=key, optional
            # producer.flush()  # scheint eine schlechte idee zu sein

    except Exception as e:
        print(f"Error: {e}")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    producer = Producer(conf)
    TOPICS = ["sensor_1", "sensor_2", "sensor_3"]
    SLEEP_TIME = (1, 2)

    print("START PRODUCE")
    start_produce(producer)
