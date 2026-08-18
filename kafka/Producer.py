import  json
from kafka import KafkaProducer
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

def create_evennt(producer,user:GitHubProfile,job_description:str,tech_stack):
        """Create an event"""
        try:
            for users in user:
                producer.send(
                    topic='github_events',
                    value=users,
                )
        except(Exception e):
            logger.error("error in creating event")
