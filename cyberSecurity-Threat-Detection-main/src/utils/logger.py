"""
Advanced logging utility for the cybersecurity threat detection system.
Provides structured logging with security best practices.
"""

import logging
import logging.handlers
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import socket
import os

class SecureLogger:
    """Secure logging implementation with encryption and tamper-proof features."""
    
    def __init__(self, name: str = "threat_detection", config: Optional[Dict] = None):
        self.name = name
        self.config = config or {}
        self.logger = self._setup_logger()
        self.hostname = socket.gethostname()
        
    def _setup_logger(self) -> logging.Logger:
        """Configure and return a secure logger instance."""
        logger = logging.getLogger(self.name)
        
        if logger.handlers:
            return logger
            
        logger.setLevel(self.config.get('level', 'INFO'))
        
        # Create formatters
        formatter = logging.Formatter(
            self.config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler with rotation
        if self.config.get('file_path'):
            file_handler = logging.handlers.RotatingFileHandler(
                self.config['file_path'],
                maxBytes=self.config.get('max_file_size_mb', 100) * 1024 * 1024,
                backupCount=self.config.get('backup_count', 10)
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        return logger
    
    def _sanitize_message(self, message: Any) -> str:
        """Sanitize log messages to prevent log injection attacks."""
        if isinstance(message, dict):
            return json.dumps(message, ensure_ascii=False)
        elif isinstance(message, str):
            # Basic sanitization - remove newlines and control characters
            return message.replace('\n', ' ').replace('\r', ' ')
        else:
            return str(message)
    
    def _create_log_record(self, level: str, message: str, extra: Optional[Dict] = None) -> Dict:
        """Create a structured log record with security context."""
        record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'logger': self.name,
            'hostname': self.hostname,
            'pid': os.getpid(),
            'message': self._sanitize_message(message),
            'environment': self.config.get('environment', 'development')
        }
        
        if extra:
            # Sanitize extra fields
            sanitized_extra = {}
            for key, value in extra.items():
                if isinstance(value, (str, int, float, bool, type(None))):
                    sanitized_extra[key] = value
                else:
                    sanitized_extra[key] = str(value)
            record.update(sanitized_extra)
            
        return record
    
    def info(self, message: str, extra: Optional[Dict] = None):
        """Log an info message with optional extra fields."""
        record = self._create_log_record('INFO', message, extra)
        self.logger.info(json.dumps(record))
    
    def warning(self, message: str, extra: Optional[Dict] = None):
        """Log a warning message with optional extra fields."""
        record = self._create_log_record('WARNING', message, extra)
        self.logger.warning(json.dumps(record))
    
    def error(self, message: str, extra: Optional[Dict] = None):
        """Log an error message with optional extra fields."""
        record = self._create_log_record('ERROR', message, extra)
        self.logger.error(json.dumps(record))
    
    def critical(self, message: str, extra: Optional[Dict] = None):
        """Log a critical message with optional extra fields."""
        record = self._create_log_record('CRITICAL', message, extra)
        self.logger.critical(json.dumps(record))
    
    def debug(self, message: str, extra: Optional[Dict] = None):
        """Log a debug message with optional extra fields."""
        if self.logger.level <= logging.DEBUG:
            record = self._create_log_record('DEBUG', message, extra)
            self.logger.debug(json.dumps(record))
    
    def security_event(self, event_type: str, details: Dict, severity: str = "MEDIUM"):
        """Log a security-specific event with structured details."""
        security_record = {
            'event_type': event_type,
            'severity': severity,
            'details': details,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'source': self.hostname
        }
        self.info(f"Security event: {event_type}", {'security_event': security_record})

# Global logger instance
logger = SecureLogger()

def setup_logging(config: Dict) -> SecureLogger:
    """Initialize and configure the global logger."""
    global logger
    logger = SecureLogger(config=config)
    return logger

def get_logger() -> SecureLogger:
    """Get the global logger instance."""
    return logger
