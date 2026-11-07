"""
Main Detection Engine for the Cybersecurity Threat Detection System.
Orchestrates threat detection using multiple detection methods.
"""

import json
import random
from typing import Dict, List
from .signature_detector import SignatureDetector
from .anomaly_detector import AnomalyDetector
from .threat_classifier import ThreatClassifier
from ..utils.logger import get_logger

logger = get_logger()

class DetectionEngine:
    """Main detection engine that combines multiple detection methods."""
    
    def __init__(self):
        self.signature_detector = SignatureDetector()
        self.anomaly_detector = AnomalyDetector()
        self.threat_classifier = ThreatClassifier()
        self.threat_dataset = self._load_threat_dataset()
        logger.info("Detection Engine initialized with random detection.")

    def _load_threat_dataset(self) -> List[Dict]:
        """Load threat dataset from JSON file."""
        import os
        # Try multiple possible paths
        possible_paths = [
            'src/detection/threat_dataset.json',
            os.path.join(os.path.dirname(__file__), 'threat_dataset.json'),
            'threat_dataset.json'
        ]
        
        for path in possible_paths:
            try:
                with open(path, 'r') as f:
                    dataset = json.load(f)
                    logger.info(f"Loaded threat dataset from {path} with {len(dataset)} threats")
                    return dataset
            except FileNotFoundError:
                continue
        
        logger.warning("Threat dataset not found, using default signatures.")
        return [
            {"threat_type": "malware", "risk_score": 90},
            {"threat_type": "phishing", "risk_score": 85},
            {"threat_type": "brute_force", "risk_score": 80}
        ]
    
    def detect_threats(self, data: Dict) -> List[Dict]:
        """Detect threats based on input data patterns and characteristics."""
        if not self.threat_dataset:
            logger.warning("No threat dataset available.")
            return []
        
        detected_threats = []
        input_port = data.get('port', 80)
        input_protocol = data.get('protocol', 'TCP')
        input_payload_size = data.get('payload_size', 1000)
        input_request_type = data.get('request_type', 'GET')
        input_source_ip = data.get('source_ip', '192.168.1.1')
        
        # Extract IP prefix for pattern matching
        source_ip_prefix = '.'.join(input_source_ip.split('.')[:2])
        
        logger.info(f"Analyzing input: Port={input_port}, Protocol={input_protocol}, Payload={input_payload_size}, Request={input_request_type}, Source={source_ip_prefix}")
        
        # Score each threat based on pattern matching
        threat_scores = []
        for threat in self.threat_dataset:
            score = self._calculate_threat_score(threat, {
                'port': input_port,
                'protocol': input_protocol,
                'payload_size': input_payload_size,
                'request_type': input_request_type,
                'source_ip_prefix': source_ip_prefix
            })
            
            if score > 0:
                threat_scores.append((threat, score))
                logger.info(f"Threat '{threat.get('attack_name')}' scored {score} points")
        
        # Sort by score and select the highest scoring threat
        if threat_scores:
            threat_scores.sort(key=lambda x: x[1], reverse=True)
            best_threat, best_score = threat_scores[0]
            
            # Only report if score is above threshold
            if best_score >= 3:  # Minimum threshold for detection
                threat = self._create_threat_response(best_threat, data, best_score)
                detected_threats.append(threat)
                logger.info(f"Smart threat detected: {threat['name']} - {threat['threat_type']} (Score: {best_score})")
            else:
                logger.info(f"No threats detected (best score {best_score} below threshold)")
        else:
            logger.info("No threats detected (no matching patterns)")
        
        return detected_threats
    
    def _calculate_threat_score(self, threat: Dict, input_data: Dict) -> int:
        """Calculate threat score based on pattern matching."""
        score = 0
        patterns = threat.get('detection_patterns', {})
        
        # Port matching (highest weight)
        if input_data['port'] in patterns.get('ports', []):
            score += 3
        elif abs(input_data['port'] - threat.get('port', 80)) <= 10:
            score += 1
        
        # Protocol matching
        if input_data['protocol'] in patterns.get('protocols', []):
            score += 2
        elif input_data['protocol'] == threat.get('protocol', 'TCP'):
            score += 1
        
        # Payload size matching
        if patterns.get('payload_sizes'):
            min_size, max_size = patterns['payload_sizes']
            if min_size <= input_data['payload_size'] <= max_size:
                score += 2
        elif abs(input_data['payload_size'] - threat.get('payload_size', 1000)) <= 500:
            score += 1
        
        # Request type matching
        if input_data['request_type'] in patterns.get('request_types', []):
            score += 2
        elif input_data['request_type'] == threat.get('request_type', 'GET'):
            score += 1
        
        # Source IP prefix matching
        if input_data['source_ip_prefix'] in patterns.get('source_ips', []):
            score += 1
        
        return score
    
    def _create_threat_response(self, threat: Dict, input_data: Dict, score: int) -> Dict:
        """Create threat response object."""
        # Determine severity based on risk_score
        risk_score = threat.get('risk_score', 50)
        if risk_score >= 80:
            severity = "critical"
        elif risk_score >= 60:
            severity = "high"
        elif risk_score >= 40:
            severity = "medium"
        else:
            severity = "low"
        
        # Calculate confidence based on pattern matching score
        confidence = min(95, 60 + (score * 8))  # Base 60% + score-based confidence
        
        return {
            "type": "attack",
            "name": threat.get('attack_name', threat.get('threat_type', 'unknown')),
            "threat_type": threat.get('threat_type', 'unknown'),
            "risk_score": risk_score,
            "confidence": int(confidence),
            "description": threat.get('description', f"Threat detected: {threat.get('threat_type', 'unknown')}"),
            "severity": severity,
            "solutions": threat.get('solutions', []),
            "attack_details": {
                "protocol": input_data.get('protocol', 'TCP'),
                "port": input_data.get('port', 80),
                "payload_size": input_data.get('payload_size', 1000),
                "request_type": input_data.get('request_type', 'GET')
            },
            "detection_score": score,
            "timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp
        }
    
    def update_signatures(self, signatures: List[Dict]):
        """Update the signature database."""
        self.signature_detector.update_signatures(signatures)
        logger.info("Signatures updated.")
    
    def train_models(self, training_data: List[Dict]):
        """Train the machine learning models."""
        self.anomaly_detector.train(training_data)
        self.threat_classifier.train(training_data)
        logger.info("Models trained.")

if __name__ == "__main__":
    engine = DetectionEngine()
    test_data = {"source_ip": "192.168.1.1", "destination_ip": "192.168.1.2"}
    threats = engine.detect_threats(test_data)
    print(threats)
