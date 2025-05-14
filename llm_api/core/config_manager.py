import os
import json
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Manages configuration for different LLM providers.
    Supports loading from environment variables and JSON files.
    """
    
    @staticmethod
    def load_config(
        provider_name: str, 
        config_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Load configuration for a specific provider.
        
        :param provider_name: Name of the LLM provider
        :param config_path: Optional path to config file
        :return: Configuration dictionary
        """
        # First, try environment variables
        env_config = ConfigManager._load_env_config(provider_name)
        if env_config:
            return env_config
        
        # Then, try config file
        if config_path and os.path.exists(config_path):
            return ConfigManager._load_json_config(config_path)
        
        # Default empty config
        return {}
    
    @staticmethod
    def _load_env_config(provider_name: str) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        :param provider_name: Name of the LLM provider
        :return: Configuration dictionary from environment
        """
        prefix = f"{provider_name.upper()}_"
        return {
            key.replace(prefix, '').lower(): value
            for key, value in os.environ.items()
            if key.startswith(prefix)
        }
    
    @staticmethod
    def _load_json_config(config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        :param config_path: Path to configuration JSON file
        :return: Configuration dictionary from JSON
        """
        with open(config_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_config(
        provider_name: str, 
        config: Dict[str, Any], 
        config_path: Optional[str] = None
    ) -> None:
        """
        Save configuration to a JSON file.
        
        :param provider_name: Name of the LLM provider
        :param config: Configuration dictionary
        :param config_path: Optional path to save config file
        """
        if config_path:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
