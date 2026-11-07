"""
Kafka Consumer for the Cybersecurity Threat Detection System.
Handles real-time data streaming from Kafka topics.
"""

from kafka import KafkaProducer
from typing import Dict
import json
from ..utils.logger import get_logger

logger = get_logger()

class KafkaConsumer:
    """Kafka consumer for ingesting data from topics."""
    
    def __init__(self, topic: str, bootstrap_servers: str = "localhost:9092"):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def send(self, data: Dict):
        """Send data to Kafka topic."""
        try:
            self.producer.send(self.topic, value=data)
            self.producer.flush()
            logger.info(f"Data sent to Kafka topic {self.topic}: {data}")
        except Exception as e:
            logger.error(f"Error sending data to Kafka: {str(e)}")
    
    def close(self):
        """Close the Kafka producer."""
        self.producer.close()
        logger.info("Kafka producer closed.")

if __name__ == "__main__":
    consumer = KafkaConsumer(topic="network_traffic")
    test_data = {"test": "data"}
    consumer.send(test_data)
    consumer.close()
