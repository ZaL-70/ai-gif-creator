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
    MAX_PROMPT_LENGTH = 350
    GIF_DURATION = 3  # seconds
    GIF_FPS = 10
    MAX_FILE_SIZE_MB = 8
    
    # Video Resolution Settings
    RESOLUTION_QUALITY = "low"  # Options: "low", "medium", "high"
    RESOLUTION_MAP = {
        "low": "480p",
        "medium": "720p",
        "high": "1080p"
    }

    # Paths
    TEMP_DIR = 'temp'
    
    # Prompt Templates
    PROMPT_TEMPLATE = "You are a sentient meme engine that interprets human requests with maximal absurdity. You combine surrealism, meme logic, and chaotic dreamlike visual comedy. Every video should feel like it escaped from an alternate reality where humour evolved without context. Apply Gen Z absurdist humor. Now create the gif based on the following prompt: {user_prompt}"
    IMAGE_PROMPT_TEMPLATE = "Analyze this image thoroughly, then transform it into pure brainrot content - the kind of absurdist, surreal Instagram Reel that makes no logical sense but is hypnotically entertaining. Apply Gen Z absurdist humor, ironic detachment, and that specific unhinged energy that defines modern internet culture. Now transform the image into this gif based on the following prompt: {user_prompt}"
