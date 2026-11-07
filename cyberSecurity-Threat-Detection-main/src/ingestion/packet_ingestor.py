"""
Packet Ingestor for the Cybersecurity Threat Detection System.
Processes PCAP files and live network traffic for analysis.
"""

import scapy.all as scapy
from typing import List, Dict
from .kafka_consumer import KafkaConsumer
from .data_normalizer import normalize_packet
from ..utils.logger import get_logger

logger = get_logger()

class PacketIngestor:
    """Ingests packets from live traffic or PCAP files."""
    
    def __init__(self, kafka_topic: str):
        self.kafka_topic = kafka_topic
        self.consumer = KafkaConsumer(topic=self.kafka_topic)
    
    def start_live_capture(self):
        """Start capturing live packets."""
        logger.info("Starting live packet capture...")
        scapy.sniff(prn=self.process_packet, store=False)
    
    def process_packet(self, packet: scapy.Packet):
        """Process a single packet."""
        try:
            normalized_data = normalize_packet(packet)
            self.send_to_kafka(normalized_data)
        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")
    
    def send_to_kafka(self, data: Dict):
        """Send normalized packet data to Kafka."""
        self.consumer.send(data)
        logger.info(f"Packet sent to Kafka: {data}")

    def stop_capture(self):
        """Stop the packet capture."""
        logger.info("Stopping packet capture...")
        scapy.sniff(stop_filter=lambda x: False)  # This will stop the capture

if __name__ == "__main__":
    ingestor = PacketIngestor(kafka_topic="network_traffic")
    ingestor.start_live_capture()
