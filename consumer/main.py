from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

conf = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "foo",
    "auto.offset.reset": "smallest",
}

consumer = Consumer(conf)


def consume_forever(consumer, topics):
    try:
        consumer.subscribe(topics)
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            print("msg:", msg)

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(msg.value())
                sys.stdout.flush()
    finally:
        consumer.close()


topics = ["my-topic"]
consume_forever(consumer, topics)
