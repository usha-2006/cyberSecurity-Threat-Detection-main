"""
Alert Manager for the Cybersecurity Threat Detection System.
Handles threat alerts and notifications to various channels.
"""

from typing import Dict, List
from .notification_service import NotificationService
from ..utils.logger import get_logger

logger = get_logger()

class AlertManager:
    """Manages threat alerts and notifications."""
    
    def __init__(self):
        self.notification_service = NotificationService()
        logger.info("Alert Manager initialized.")
    
    def process_alerts(self, threats: List[Dict]):
        """Process and send alerts for detected threats."""
        for threat in threats:
            self._send_alert(threat)
    
    def _send_alert(self, threat: Dict):
        """Send an alert for a single threat."""
        alert_message = self._create_alert_message(threat)
        
        # Determine alert severity based on risk score
        risk_score = threat.get("risk_score", 0)
        if risk_score >= 90:
            severity = "CRITICAL"
        elif risk_score >= 70:
            severity = "HIGH"
        elif risk_score >= 50:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        # Send notifications
        self.notification_service.send_email(alert_message, severity)
        self.notification_service.send_slack(alert_message, severity)
        
        logger.info(f"Alert sent: {alert_message}")
    
    def _create_alert_message(self, threat: Dict) -> str:
        """Create a formatted alert message."""
        return f"""
        THREAT ALERT
        Type: {threat.get('type', 'unknown')}
        Risk Score: {threat.get('risk_score', 0)}
        Description: {threat.get('description', 'No description')}
        Confidence: {threat.get('confidence', 'unknown')}
        """

if __name__ == "__main__":
    alert_manager = AlertManager()
    test_threat = {
        "type": "malware",
        "risk_score": 95,
        "description": "Malware detected in network traffic",
        "confidence": "high"
    }
    alert_manager.process_alerts([test_threat])
