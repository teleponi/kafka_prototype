"""
Kafka Consumer Beispiel

Eingehende Sensordaten der Fertiungsmaschinen werden hier eingelesen
und beispielhaft die NAN-Werte, die von den Sensoren gesendet werden, 
herausgefiltert.
"""
import json
import math
import logging
from confluent_kafka import Consumer, KafkaError, cimpl

conf = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "foo",
    "auto.offset.reset": "smallest",
}

consumer = Consumer(conf)

logger = logging.Logger("consumer")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def process_input(msg: cimpl.Message) -> None:
    """Process incoming Sensor data.

    Args:
        msg: Json String 
    """
    try:
        msg_decoded = json.loads(msg.value().decode("utf-8"))
        if math.isnan(msg_decoded["temp"]):
            logger.info("nan value detected")
        else:
            logger.info(msg_decoded)
    except Exception as e:
        logger.warning(f"error processing: {e}")


def consume_forever(consumer: Consumer, topics: list[str]) -> None:
    """Main Consumer Loop.

    This is an example of a consumer, that keeps polling data from
    the Kafka Cluster.

    Args:
        consumer: Kafka Consumer
        topics: topiclist
    """
    try:
        consumer.subscribe(topics)
        while True:
            msg: cimpl.Message = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.error(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    logger.error(msg.error())
            else:
                process_input(msg)
    except Exception as e:
        logger.critical(f"Kafka Error: {e}")
    finally:
        logger.info("Consumer is closing")
        consumer.close()


topics = ["sensor_1", "sensor_2", "sensor_3"]
logger.info(f"Start Consuming these topics: {topics}")
consume_forever(consumer, topics)
