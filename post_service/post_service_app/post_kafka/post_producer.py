from kafka import KafkaProducer
import json

from post_service_app.config import KAFKA_BOOTSTRAP_SERVERS

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: str(v).encode('utf-8') if v else None
)

def send_event(topic: str, event_data: dict, key: str = None):
    producer.send(topic, value=event_data, key=key)
    producer.flush()