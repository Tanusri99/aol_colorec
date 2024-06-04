from kafka import KafkaProducer
import json

def send_to_kafka(topic, data):
    """
    Sends data to a Kafka topic.

    Args:
        topic (str): The name of the Kafka topic to send the data to.
        data (Any): The data to be sent to the Kafka topic.

    Returns:
        None
    """
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092', 
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic, value=data)
    producer.flush()
    producer.close()
    
