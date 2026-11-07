"""
Configuration loader with security validation and environment-specific settings.
Supports YAML configuration files with environment variable overrides.
"""

import yaml
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from .logger import get_logger

class ConfigLoader:
    """Secure configuration loader with validation and environment support."""
    
    def __init__(self):
        self.logger = get_logger()
        self.config: Dict[str, Any] = {}
        self.env_vars_prefix = "THREAT_DETECTION_"
        
    def load_config(self, config_path: str, environment: str = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file with environment-specific overrides.
        
        Args:
            config_path: Path to the configuration file
            environment: Environment name (development, production, etc.)
            
        Returns:
            Loaded configuration dictionary
        """
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
                
            with open(config_path, 'r') as f:
                base_config = yaml.safe_load(f) or {}
                
            # Apply environment-specific overrides
            env_config = self._get_environment_config(base_config, environment)
            
            # Apply environment variable overrides
            final_config = self._apply_env_vars(env_config)
            
            # Validate configuration
            self._validate_config(final_config)
            
            self.config = final_config
            self.logger.info(f"Configuration loaded successfully from {config_path}")
            return final_config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            raise
            
    def _get_environment_config(self, base_config: Dict, environment: str) -> Dict:
        """Get environment-specific configuration."""
        if not environment:
            environment = os.getenv('ENVIRONMENT', 'development')
            
        env_config = base_config.copy()
        
        # Merge environment-specific settings
        if 'environments' in base_config and environment in base_config['environments']:
            env_specific = base_config['environments'][environment]
            self._deep_merge(env_config, env_specific)
            
        return env_config
    
    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Recursively merge two dictionaries."""
        for key, value in update.items():
            if (key in base and isinstance(base[key], dict) and 
                isinstance(value, dict)):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _apply_env_vars(self, config: Dict) -> Dict:
        """Override configuration with environment variables."""
        config_copy = config.copy()
        self._apply_env_vars_recursive(config_copy, "")
        return config_copy
    
    def _apply_env_vars_recursive(self, config_node: Any, path: str) -> None:
        """Recursively apply environment variable overrides."""
        if isinstance(config_node, dict):
            for key, value in config_node.items():
                new_path = f"{path}_{key}" if path else key
                self._apply_env_vars_recursive(value, new_path)
        elif isinstance(config_node, list):
            for i, item in enumerate(config_node):
                new_path = f"{path}_{i}"
                self._apply_env_vars_recursive(item, new_path)
        else:
            env_var_name = f"{self.env_vars_prefix}{path.upper()}"
            env_value = os.getenv(env_var_name)
            if env_value is not None:
                # Try to convert to appropriate type
                try:
                    if isinstance(config_node, bool):
                        config_node = env_value.lower() in ('true', '1', 'yes')
                    elif isinstance(config_node, int):
                        config_node = int(env_value)
                    elif isinstance(config_node, float):
                        config_node = float(env_value)
                    elif isinstance(config_node, list):
                        config_node = json.loads(env_value)
                    elif isinstance(config_node, dict):
                        config_node = json.loads(env_value)
                    else:
                        config_node = env_value
                except (ValueError, json.JSONDecodeError):
                    config_node = env_value
    
    def _validate_config(self, config: Dict) -> None:
        """Validate configuration for security and completeness."""
        required_sections = ['app', 'ingestion', 'detection', 'storage', 'alerting']
        
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")
                
        # Security validation
        self._validate_security_config(config.get('security', {}))
        
        # Database connection validation
        self._validate_database_config(config.get('storage', {}))
        
    def _validate_security_config(self, security_config: Dict) -> None:
        """Validate security-related configuration."""
        if security_config.get('encryption', {}).get('enabled', False):
            if not security_config['encryption'].get('algorithm'):
                raise ValueError("Encryption algorithm must be specified when encryption is enabled")
                
        if security_config.get('ssl', {}).get('enabled', False):
            if not security_config['ssl'].get('cert_file') or not security_config['ssl'].get('key_file'):
                raise ValueError("SSL certificate and key files must be specified when SSL is enabled")
    
    def _validate_database_config(self, storage_config: Dict) -> None:
        """Validate database connection configuration."""
        if storage_config.get('elasticsearch', {}).get('hosts'):
            hosts = storage_config['elasticsearch']['hosts']
            if not isinstance(hosts, list) or not hosts:
                raise ValueError("Elasticsearch hosts must be a non-empty list")
                
        if storage_config.get('mongodb', {}).get('uri'):
            uri = storage_config['mongodb']['uri']
            if not uri.startswith(('mongodb://', 'mongodb+srv://')):
                raise ValueError("MongoDB URI must start with mongodb:// or mongodb+srv://")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key."""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def reload(self, config_path: str = None, environment: str = None) -> None:
        """Reload configuration from file."""
        if config_path is None:
            config_path = getattr(self, '_last_config_path', None)
            if config_path is None:
                raise ValueError("No configuration path specified for reload")
                
        self.load_config(config_path, environment)
        
    def to_dict(self) -> Dict[str, Any]:
        """Return the configuration as a dictionary."""
        return self.config.copy()

# Global configuration instance
_config_loader = ConfigLoader()

def load_config(config_path: str, environment: str = None) -> Dict[str, Any]:
    """Load configuration using the global config loader."""
    return _config_loader.load_config(config_path, environment)

def get_config() -> ConfigLoader:
    """Get the global configuration loader instance."""
    return _config_loader

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value by key."""
    return _config_loader.get(key, default)
