import json
from kafka import KafkaConsumer
from loguru import logger


def wait_for_Response(request_id):

    consumer = KafkaConsumer(
        'response-topic',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=f'response-group-{request_id}',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    try:
        while True:

            records = consumer.poll(timeout_ms=1000)

            for topic_partition, messages in records.items():

                for message in messages:

                    data = message.value

                    logger.info(f"Response received: {data}")
                    logger.info(f"Expected request_id: {request_id}")
                    logger.info(f"Received request_id: {data.get('request_id')}")

                    if data.get("request_id") == request_id:

                        logger.info("========== MATCH FOUND ==========")

                        return data["result"]

    finally:
        consumer.close()