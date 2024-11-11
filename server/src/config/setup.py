from src.config.logging import logger
from typing import Dict
from typing import Any 
import yaml
import os


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = None):
        """
        Initialize the Config class.

        Args:
        - config_path (str, optional): Path to the YAML configuration file.
        """
        if self.__initialized:
            return
        self.__initialized = True

        config_path = config_path or self._find_config_path()
        logger.info(f"Initializing Config with config path: {config_path}")
        
        self.__config = self._load_config(config_path)
        if self.__config:
            self.PROJECT_ID = self.__config.get('project_id')
            self.REGION = self.__config.get('region')
            self.CREDENTIALS_PATH = self._find_credentials_path()
            self.MODEL_NAME = self.__config.get('model_name')

            if self.CREDENTIALS_PATH:
                self._set_google_credentials(self.CREDENTIALS_PATH)
            else:
                logger.warning("No credentials path found; Google credentials not set.")
        else:
            logger.error("Configuration could not be loaded. Please check the file path and format.")

    @staticmethod
    def _find_config_path() -> str:
        """
        Attempts to find the config file in multiple locations.

        Returns:
        - str: Path to the found configuration file, or None if not found.
        """
        possible_paths = [
            os.path.abspath("./server/config/config.yml"),
            os.path.abspath("./config/config.yml"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Configuration file found at: {path}")
                return path
        logger.error("Configuration file not found in any default locations.")
        raise FileNotFoundError("Configuration file not found in expected locations.")

    @staticmethod
    def _find_credentials_path() -> str:
        """
        Attempts to find the credentials file in multiple locations.

        Returns:
        - str: Path to the found credentials file, or None if not found.
        """
        possible_paths = [
            os.path.abspath("./server/credentials/key.json"),
            os.path.abspath("./credentials/key.json"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Credentials file found at: {path}")
                return path
        logger.error("Credentials file not found in any default locations.")
        raise FileNotFoundError("Credentials file not found in expected locations.")

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        """
        Load the YAML configuration from the given path.

        Args:
        - config_path (str): Path to the YAML configuration file.

        Returns:
        - dict: Loaded configuration data or None if loading fails.
        """
        try:
            with open(config_path, 'r') as file:
                logger.info("Loading configuration file.")
                return yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in configuration file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading configuration file: {e}")
        return None

    @staticmethod
    def _set_google_credentials(credentials_path: str) -> None:
        """
        Set the Google application credentials environment variable.

        Args:
        - credentials_path (str): Path to the Google credentials file.
        """
        if os.path.exists(credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            logger.info(f"Google application credentials set from {credentials_path}")
        else:
            logger.error(f"Credentials file not found at {credentials_path}. Google credentials not set.")


config = Config()
