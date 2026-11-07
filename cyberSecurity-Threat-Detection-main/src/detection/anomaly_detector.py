"""
Anomaly Detector for the Cybersecurity Threat Detection System.
Uses machine learning to detect unknown threats based on anomalous behavior.
"""

from typing import Dict, List
import numpy as np
from sklearn.ensemble import IsolationForest
from ..utils.logger import get_logger

logger = get_logger()

class AnomalyDetector:
    """Detects anomalies using machine learning models."""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.is_trained = False
        logger.info("Anomaly Detector initialized.")
    
    def extract_features(self, data: Dict) -> np.ndarray:
        """Extract features from data for anomaly detection."""
        features = []
        # Example features: length of values, presence of certain patterns, etc.
        for key, value in data.items():
            if isinstance(value, str):
                features.append(len(value))
                features.append(1 if "http" in value else 0)
            elif isinstance(value, (int, float)):
                features.append(value)
        return np.array(features).reshape(1, -1)
    
    def detect(self, data: Dict) -> List[Dict]:
        """Detect anomalies in the data."""
        if not self.is_trained:
            logger.warning("Anomaly detector not trained yet.")
            return []
        
        features = self.extract_features(data)
        prediction = self.model.predict(features)
        
        if prediction[0] == -1:  # Anomaly detected
            threat = {
                "type": "anomaly",
                "risk_score": 75,  # Medium risk for anomalies
                "confidence": "medium",
                "description": "Anomalous behavior detected"
            }
            logger.info(f"Anomaly threat detected: {threat}")
            return [threat]
        return []
    
    def train(self, training_data: List[Dict]):
        """Train the anomaly detection model."""
        features = []
        for data in training_data:
            feat = self.extract_features(data)
            features.append(feat.flatten())
        
        X = np.array(features)
        self.model.fit(X)
        self.is_trained = True
        logger.info("Anomaly detection model trained.")

if __name__ == "__main__":
    detector = AnomalyDetector()
    # Mock training data
    training_data = [{"normal": "data"}, {"another": "normal"}]
    detector.train(training_data)
    
    test_data = {"suspicious": "very_long_and_suspicious_string_here"}
    threats = detector.detect(test_data)
    print(threats)
