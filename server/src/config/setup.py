from src.config.logging import logger
from typing import Dict, Any
import yaml
import os

CONFIG_PATH = './config/setup.yml'


class _Config:
    """
    Singleton class to manage application configuration.

    Attributes:
    -----------
    PROJECT_ID : str
        The project ID from the configuration file.
    REGION : str
        The region from the configuration file.
    CREDENTIALS_PATH : str
        The path to the Google credentials JSON file.
    TEXT_GEN_MODEL_NAME : str
        The name of the text generation model.

    Methods:
    --------
    _load_config(config_path: str) -> Dict[str, Any]:
        Load the YAML configuration from the given path.
    _set_google_credentials(credentials_path: str) -> None:
        Set the Google application credentials environment variable.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensure that only one instance of the _Config class is created (Singleton pattern).
        """
        if not cls._instance:
            cls._instance = super(_Config, cls).__new__(cls)
            # The following line ensures that the __init__ method is only called once.
            cls._instance.__initialized = False
        return cls._instance
    
    def __init__(self, config_path: str = CONFIG_PATH):
        """
        Initialize the _Config class by loading the configuration.

        Parameters:
        -----------
        config_path : str
            Path to the YAML configuration file.
        """
        if self.__initialized:
            return
        self.__initialized = True
        
        self.__config = self._load_config(config_path)
        self.PROJECT_ID = self.__config['project_id']
        self.REGION = self.__config['region']
        self.CREDENTIALS_PATH = self.__config['credentials_json']
        self.MODEL = self.__config['model']
        self._set_google_credentials(self.CREDENTIALS_PATH)

    @staticmethod
    def _load_config(config_path: str) -> Dict[str, Any]:
        """
        Load the YAML configuration from the given path.

        Parameters:
        -----------
        config_path : str
            Path to the YAML configuration file.

        Returns:
        --------
        Dict[str, Any]
            Loaded configuration data.

        Raises:
        -------
        Exception
            If the configuration file fails to load, logs the error.
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load the configuration file. Error: {e}")
            raise

    @staticmethod
    def _set_google_credentials(credentials_path: str) -> None:
        """
        Set the Google application credentials environment variable.

        Parameters:
        -----------
        credentials_path : str
            Path to the Google credentials file.
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


# Create a single instance of the _Config class.
config = _Config()
