from kafka import KafkaConsumer
import json
from  loguru import logger

from PorcessingKf.consumer import HandleProfiles
from data_access import GitHubProfile

# Kafka Consumer
consumer = KafkaConsumer(
    'driver-location',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from the earliest message
    enable_auto_commit=True,
    group_id='location-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize data from JSON
)

def wait_for_Response(request_id):
    for message in consumer:
        HandleProfiles()
        data = message.value
        if data['request_id'] == request_id:
           return data['result']
# Start consuming location updates
