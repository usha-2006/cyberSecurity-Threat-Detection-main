"""
Signature-based Detector for the Cybersecurity Threat Detection System.
Detects known threats using predefined signatures and patterns.
"""

from typing import Dict, List
from ..utils.logger import get_logger

logger = get_logger()

class SignatureDetector:
    """Detects known threats using signature-based methods."""
    
    def __init__(self):
        self.signatures = self._load_default_signatures()
        logger.info("Signature Detector initialized with default signatures.")
    
    def _load_default_signatures(self) -> List[Dict]:
        """Load default threat signatures."""
        return [
            {"type": "malware", "pattern": "malware.com", "risk_score": 90},
            {"type": "phishing", "pattern": "login.php", "risk_score": 85},
            {"type": "brute_force", "pattern": "failed login", "risk_score": 80}
        ]
    
    def detect(self, data: Dict) -> List[Dict]:
        """Detect threats based on signatures."""
        threats = []
        for signature in self.signatures:
            if self._matches_signature(data, signature):
                threat = {
                    "type": signature["type"],
                    "risk_score": signature["risk_score"],
                    "confidence": "high",
                    "description": f"Signature match: {signature['pattern']}"
                }
                threats.append(threat)
                logger.info(f"Signature threat detected: {threat}")
        return threats
    
    def _matches_signature(self, data: Dict, signature: Dict) -> bool:
        """Check if data matches a signature."""
        pattern = signature["pattern"]
        # Simple string matching - can be extended with regex or more complex patterns
        for value in data.values():
            if isinstance(value, str) and pattern in value:
                return True
        return False
    
    def update_signatures(self, new_signatures: List[Dict]):
        """Update the signature database."""
        self.signatures.extend(new_signatures)
        logger.info(f"Added {len(new_signatures)} new signatures.")

if __name__ == "__main__":
    detector = SignatureDetector()
    test_data = {"url": "malware.com/download"}
    threats = detector.detect(test_data)
    print(threats)
