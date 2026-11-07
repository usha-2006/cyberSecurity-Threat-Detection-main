"""
Test script for the Cybersecurity Threat Detection System.
Demonstrates the system's capabilities with sample data.
"""

import json
import time
from src.detection.detection_engine import DetectionEngine
from src.alerting.alert_manager import AlertManager
from src.utils.logger import setup_logging

# Setup logging
config = {
    "level": "INFO",
    "file_path": "./logs/test.log",
    "max_file_size_mb": 10,
    "backup_count": 5
}
setup_logging(config)

def test_detection_engine():
    """Test the detection engine with various threat scenarios."""
    print("Testing Detection Engine...")
    engine = DetectionEngine()
    
    # Test data samples
    test_cases = [
        {
            "name": "Malware Download",
            "data": {
                "url": "malware.com/download.exe",
                "source_ip": "192.168.1.100",
                "destination_ip": "10.0.0.1"
            },
            "expected_threats": 1
        },
        {
            "name": "Phishing Attempt",
            "data": {
                "url": "login.php?user=admin",
                "email": "phishing@fake-bank.com",
                "content": "Please verify your account credentials"
            },
            "expected_threats": 1
        },
        {
            "name": "Normal Traffic",
            "data": {
                "url": "google.com/search",
                "source_ip": "192.168.1.101",
                "destination_ip": "8.8.8.8"
            },
            "expected_threats": 0
        },
        {
            "name": "Suspicious Anomaly",
            "data": {
                "behavior": "very_unusual_and_suspicious_pattern_detected_here",
                "frequency": 1000,
                "duration": 300
            },
            "expected_threats": 1
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input: {json.dumps(test_case['data'], indent=2)}")
        
        threats = engine.detect_threats(test_case['data'])
        print(f"Detected Threats: {len(threats)}")
        
        for threat in threats:
            print(f"  - Type: {threat.get('type', 'unknown')}")
            print(f"    Risk Score: {threat.get('risk_score', 0)}")
            print(f"    Description: {threat.get('description', 'No description')}")
        
        if len(threats) == test_case['expected_threats']:
            print("✓ Test PASSED")
        else:
            print("✗ Test FAILED")
        
        time.sleep(0.5)  # Brief pause between tests

def test_alert_system():
    """Test the alerting system."""
    print("\nTesting Alert System...")
    alert_manager = AlertManager()
    
    # Test threats
    test_threats = [
        {
            "type": "malware",
            "risk_score": 95,
            "description": "High-risk malware detected",
            "confidence": "high"
        },
        {
            "type": "phishing",
            "risk_score": 85,
            "description": "Phishing attempt detected",
            "confidence": "medium"
        },
        {
            "type": "brute_force",
            "risk_score": 75,
            "description": "Multiple failed login attempts",
            "confidence": "high"
        }
    ]
    
    print("Sending test alerts...")
    alert_manager.process_alerts(test_threats)
    print("Alerts processed successfully")

def test_end_to_end():
    """Test the complete system from data ingestion to alerting."""
    print("\nTesting End-to-End Workflow...")
    
    engine = DetectionEngine()
    alert_manager = AlertManager()
    
    # Simulate data coming from various sources
    data_sources = [
        # Network traffic
        {"source_ip": "192.168.1.1", "dest_ip": "malicious-site.com", "protocol": "TCP"},
        # Log data
        {"event": "failed_login", "user": "admin", "attempts": 10},
        # Web traffic
        {"url": "legitimate-site.com", "referrer": "google.com"},
        # Suspicious activity
        {"behavior": "data_exfiltration", "size": "2GB", "destination": "external-server.com"}
    ]
    
    for i, data in enumerate(data_sources):
        print(f"\nProcessing data sample {i + 1}:")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        # Detect threats
        threats = engine.detect_threats(data)
        print(f"Threats detected: {len(threats)}")
        
        # Send alerts
        if threats:
            alert_manager.process_alerts(threats)
            print("Alerts sent for detected threats")
        else:
            print("No threats detected - no alerts sent")
        
        time.sleep(0.3)

def performance_test():
    """Test system performance with multiple requests."""
    print("\nTesting Performance...")
    engine = DetectionEngine()
    
    start_time = time.time()
    requests = 100
    
    for i in range(requests):
        data = {"test": f"request_{i}", "value": i % 50}
        engine.detect_threats(data)
    
    end_time = time.time()
    total_time = end_time - start_time
    requests_per_second = requests / total_time
    
    print(f"Processed {requests} requests in {total_time:.2f} seconds")
    print(f"Throughput: {requests_per_second:.2f} requests/second")

if __name__ == "__main__":
    print("=" * 60)
    print("CYBERSECURITY THREAT DETECTION SYSTEM - TEST SUITE")
    print("=" * 60)
    
    try:
        test_detection_engine()
        test_alert_system()
        test_end_to_end()
        performance_test()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        raise
