from math import log

from etl.AgentTech import AiAgent_checkTech
from etl.RepoAiAgent import AiAgent_RepoSelect
from kafka import KafkaConsumer
import json
from  loguru import logger

from data_access import GitHubProfile
from PorcessingKf.Producer import create_producer
from etl.create_user import createUser

# Kafka Consumer
consumer = KafkaConsumer(
    'driver-location',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from the earliest message
    enable_auto_commit=True,
    group_id='location-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize data from JSON
)
producer = create_producer()
def HandleProfiles():
    logger.info("je recoit le data")
    for message in consumer:
        
        request = message.value
        request_id = message['request_id']
        profiles = message['profiles']
        job_description = message['job']
        teck_stack = message['techStack']
        # To add the the result in the list of GithubProfiles
        profiles_fin : GitHubProfile=[]
        logger.info(f"proocess the profiles {message}")
        for profiel in profiles:
            logger.info(f"profiel the profiles {profiel}")
            user = createUser(profiel)
            result = AiAgent_RepoSelect(teck_stack,job_description,user)
            profiles_fin.append(result)
        producer.send(
            "response-topic",
        value={
            "request_id": request_id,
            "results": profiles_fin
        }
        )
        producer.flush()
# Start consuming location updates
HandleProfiles()
    