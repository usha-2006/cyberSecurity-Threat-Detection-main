"""
Simple API test script that tests the core functionality without full server startup
"""

import sys
sys.path.insert(0, '.')

from src.detection.detection_engine import DetectionEngine
from src.alerting.alert_manager import AlertManager
from src.utils.logger import setup_logging

# Setup logging
setup_logging({'level': 'INFO', 'file_path': './logs/api_test.log'})

def test_detection_engine():
    """Test the detection engine directly"""
    print("Testing Detection Engine...")
    engine = DetectionEngine()
    
    # Test with various data samples
    test_cases = [
        {"url": "malware.com/download", "source_ip": "192.168.1.100"},
        {"event": "failed_login", "user": "admin", "attempts": 15},
        {"url": "google.com/search", "query": "normal search"},
        {"behavior": "unusual_pattern_detected_here_very_long_string"}
    ]
    
    for i, data in enumerate(test_cases, 1):
        print(f"\nTest {i}: {data}")
        threats = engine.detect_threats(data)
        print(f"Threats detected: {len(threats)}")
        for threat in threats:
            print(f"  - {threat}")

def test_alert_manager():
    """Test the alert manager directly"""
    print("\nTesting Alert Manager...")
    manager = AlertManager()
    
    test_threats = [
        {
            "type": "malware",
            "risk_score": 95,
            "description": "Malware download detected",
            "confidence": "high"
        },
        {
            "type": "brute_force",
            "risk_score": 85,
            "description": "Multiple failed login attempts",
            "confidence": "medium"
        }
    ]
    
    print("Sending test alerts...")
    manager.process_alerts(test_threats)
    print("Alerts processed successfully")

if __name__ == "__main__":
    print("=" * 60)
    print("API COMPONENT TESTING")
    print("=" * 60)
    
    try:
        test_detection_engine()
        test_alert_manager()
        print("\n" + "=" * 60)
        print("ALL API COMPONENT TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
