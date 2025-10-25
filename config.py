"""
Configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Discord
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')

    # API Keys
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

    # GIF Settings
    MAX_PROMPT_LENGTH = 200
    GIF_DURATION = 3  # seconds
    GIF_FPS = 10
    MAX_FILE_SIZE_MB = 8

    # Paths
    TEMP_DIR = 'temp'
    
    # Prompt
    PROMPT_TEMPLATE = "a whimsical, funny, absurd, silly, vibrant colors, meme, goofy, brainrot style {user_prompt}"
