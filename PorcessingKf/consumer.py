import json
from dataclasses import asdict
from kafka import KafkaConsumer
from loguru import logger

from PorcessingKf.Producer import create_producer
from data_access.Profile_mongo import GitHubProfile
from etl.create_user import createUser
from etl.RepoAiAgent import AiAgent_RepoSelect


def HandleProfiles():

    consumer = KafkaConsumer(
        'driver-location',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='profile-processing-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    producer = create_producer()

    logger.info("Profile consumer started")

    for message in consumer:

        request = message.value

        request_id = request['request_id']
        profiles = request['profiles']
        job_description = request['job']
        tech_stack = request['techStack']

        logger.info(f"Processing request {request_id}")

        profiles_fin : GitHubProfile= []

        for profile in profiles:

            user = createUser(profile)

            result = AiAgent_RepoSelect(
                tech_stack,
                job_description,
                user
            )
            profiles_fin.append(result)
        logger.info(f"the fina",profiles_fin)
        producer.send(
            "response-topic",
            value={
                "request_id": request_id,
                "result": [p.model_dump(mode="json") for p in profiles_fin]
            }
        )

        producer.flush()

        logger.info(
            f"Response sent for request {request_id}"
        )
if __name__ == "__main__":
    HandleProfiles()