from kafka import KafkaProducer
import json

from user_service_app.config import KAFKA_BOOTSTRAP_SERVERS

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    key_serializer=lambda x: str(x).encode('utf-8') if x else None
)

def send_event(topic: str, event_data: dict, key: str = None):
    producer.send(topic, key=key, value=event_data)
    producer.flush()