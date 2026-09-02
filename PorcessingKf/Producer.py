import  json
import random
import uuid
from kafka import KafkaProducer, producer
import time
from loguru import logger

from data_access import GitHubProfile


def create_producer():
    """Create a connection to the Kafka broker"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    return producer

def send_location_updates(profile: list , job_descriptoin: str,techStack):
    request_id = str(uuid.uuid4())
    producer = create_producer()
    data = {
                'request_id':request_id,
                "profiles":profile,
                "job":job_descriptoin,
                "techStack":techStack
            }
    logger.info(f"the data is send {data}")
    producer.send('data', data)
    producer.flush()
    return request_id

# Start sending updates for driver_id = 101

