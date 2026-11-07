"""
Threat Classifier for the Cybersecurity Threat Detection System.
Classifies detected threats into specific categories with risk scores.
"""

from typing import Dict, List
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from ..utils.logger import get_logger

logger = get_logger()

class ThreatClassifier:
    """Classifies threats into specific categories with risk assessment."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
        self.threat_types = [
            "malware", "phishing", "brute_force", "anomaly",
            "sql_injection", "xss", "ddos", "ransomware",
            "man_in_the_middle", "zero_day", "spyware", "trojan",
            "worm", "rootkit", "keylogger", "adware"
        ]
        logger.info("Threat Classifier initialized.")
    
    def protocol_to_int(self, protocol: str) -> int:
        mapping = {"TCP": 1, "UDP": 2, "ICMP": 3, "HTTP": 4, "HTTPS": 5, "SSH": 6, "RDP": 7, "DNS": 8, "SMB": 9, "FTP": 10, "SMTP": 11, "Telnet": 12, "NetBIOS": 13}
        return mapping.get(protocol.upper(), 0)
    
    def request_type_to_int(self, request_type: str) -> int:
        mapping = {"GET": 1, "POST": 2, "PUT": 3, "DELETE": 4}
        return mapping.get(request_type.upper(), 0)
    
    def extract_features(self, threat: Dict) -> np.ndarray:
        """Extract features from threat data for classification."""
        features = []
        features.append(threat.get("risk_score", 0))
        features.append(1 if "http" in str(threat.get("description", "")).lower() else 0)
        features.append(len(str(threat.get("description", ""))))
        features.append(self.protocol_to_int(threat.get("protocol", "")))
        features.append(threat.get("port", 0))
        features.append(threat.get("payload_size", 0))
        features.append(self.request_type_to_int(threat.get("request_type", "")))
        return np.array(features).reshape(1, -1)
    
    def classify(self, threats: List[Dict]) -> List[Dict]:
        """Classify threats into specific categories."""
        if not self.is_trained:
            logger.warning("Threat classifier not trained yet. Using basic classification.")
            return self._basic_classify(threats)
        
        classified_threats = []
        for threat in threats:
            features = self.extract_features(threat)
            prediction = self.model.predict(features)
            threat_type = self.threat_types[prediction[0]]
            
            classified_threat = threat.copy()
            classified_threat["classified_type"] = threat_type
            classified_threats.append(classified_threat)
            logger.info(f"Threat classified as: {threat_type}")
        
        return classified_threats
    
    def _basic_classify(self, threats: List[Dict]) -> List[Dict]:
        """Basic classification when model is not trained."""
        for threat in threats:
            threat["classified_type"] = threat.get("type", "unknown")
        return threats
    
    def train(self, dataset_path: str = "src/detection/threat_dataset.json"):
        """Train the threat classification model using dataset JSON."""
        try:
            import json
            with open(dataset_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
            # Map threat_type to integer labels
            label_map = {t: i for i, t in enumerate(self.threat_types)}
            df['label'] = df['threat_type'].map(label_map)
            
            # Prepare features
            X = df[['risk_score', 'has_http', 'description_length', 'protocol', 'port', 'payload_size', 'request_type']].copy()
            # Convert protocol and request_type to int using mapping functions
            X['protocol'] = X['protocol'].apply(self.protocol_to_int)
            X['request_type'] = X['request_type'].apply(self.request_type_to_int)
            y = df['label']
            
            self.model.fit(X, y)
            self.is_trained = True
            logger.info("Threat classification model trained with JSON dataset.")
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            self.is_trained = False

if __name__ == "__main__":
    classifier = ThreatClassifier()
    classifier.train()  # Train with dataset
    
    test_threats = [{"type": "malware", "risk_score": 90, "description": "http://malware.com", "protocol": "TCP", "port": 80, "payload_size": 1500, "request_type": "GET"}]
    classified = classifier.classify(test_threats)
    print(classified)
