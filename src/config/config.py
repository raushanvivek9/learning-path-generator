"""
Configuration module for the Learning Path Generator.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Model Configuration
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4o-mini')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2048'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Application Configuration
    APP_NAME = "Learning Path Generator"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-powered Personalized Learning Path Generator"
    
    # UI Configuration
    PAGE_LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is set"""
        if not Config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found. Please set it in your .env file"
            )
        return True


# Validate configuration on import
try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
