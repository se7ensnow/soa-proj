import json
import logging
from datetime import datetime
from kafka import KafkaConsumer
from clickhouse_connect.driver import Client

from stats_service_app.config import KAFKA_BOOTSTRAP_SERVERS
from stats_service_app.crud import insert_event

TOPIC_TO_TYPE = {
    "add_view": "view",
    "add_like": "like",
    "add_comment": "comment",
}

def run_consumer(client: Client):
    consumer = KafkaConsumer(
        *TOPIC_TO_TYPE.keys(),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='stats-service',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    for message in consumer:
        try:
            event = message.value
            topic = message.topic
            event_type = TOPIC_TO_TYPE.get(topic)

            if not event_type:
                logging.warning(f"[Kafka] Неизвестный топик: {topic}")
                continue

            user_id = event['user_id']
            post_id = event['post_id']
            timestamp = datetime.fromisoformat(event['timestamp'])
            insert_event(
                client=client,
                user_id=user_id,
                post_id=post_id,
                event_type=event_type,
                timestamp=timestamp,
            )

        except Exception as e:
            logging.exception(f"[Kafka] Ошибка при обработке сообщения: {e}")