import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'driver-location',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='location-group-test',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consumer créé")

while True:
    print("Waiting for messages...")

    records = consumer.poll(timeout_ms=1000)

    print("Records:", records)

    for topic_partition, messages in records.items():
        for message in messages:
            print("MESSAGE RECU :", message.value)
            print("Partition :", message.partition)
            print("Offset :", message.offset)