"""
Data Normalizer for the Cybersecurity Threat Detection System.
Standardizes input data formats to JSON for consistent processing.
"""

import scapy.all as scapy
from typing import Dict, Any
from ..utils.logger import get_logger

logger = get_logger()

def normalize_packet(packet: scapy.Packet) -> Dict[str, Any]:
    """Normalize a packet to a standardized JSON format."""
    try:
        normalized = {
            "timestamp": packet.time,
            "source_ip": packet[scapy.IP].src if scapy.IP in packet else None,
            "destination_ip": packet[scapy.IP].dst if scapy.IP in packet else None,
            "protocol": packet[scapy.IP].proto if scapy.IP in packet else None,
            "length": len(packet),
            "payload": str(packet.payload) if packet.payload else None
        }
        logger.info(f"Packet normalized: {normalized}")
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing packet: {str(e)}")
        return {}

def normalize_log(log: str) -> Dict[str, Any]:
    """Normalize a log entry to a standardized JSON format."""
    try:
        # Basic log normalization - can be extended based on log format
        normalized = {
            "log": log,
            "timestamp": None,  # Extract timestamp from log if possible
            "source": "unknown"
        }
        logger.info(f"Log normalized: {normalized}")
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing log: {str(e)}")
        return {}

if __name__ == "__main__":
    # Test with a sample packet
    packet = scapy.IP(src="192.168.1.1", dst="192.168.1.2") / scapy.TCP()
    normalized = normalize_packet(packet)
    print(normalized)
