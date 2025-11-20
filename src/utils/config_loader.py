"""
Load configuration from JSON files.
"""
import json
import os
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ConfigLoader:
    """Load and manage JSON configurations."""
    
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found at {self.config_path}")
            return self._default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "spatial": {"safety_buffer_distance": 50.0},
            "temporal": {"time_step": 1.0},
            "visualization": {"plot_dpi": 100},
            "logging": {"level": "INFO"}
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation (e.g., 'spatial.safety_buffer_distance')."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value else default


# Global config loader instance
_config_loader = None

def get_config_loader() -> ConfigLoader:
    """Get or create global config loader."""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader