import replicate
import os
from config import Config

def generate_video(user_prompt, image=None):
    # Set Replicate API token from config
    os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
    
    # Get resolution from config
    resolution = Config.RESOLUTION_MAP[Config.RESOLUTION_QUALITY]
    
    # Truncate prompt if it exceeds max length
    if len(user_prompt) > Config.MAX_PROMPT_LENGTH:
        user_prompt = user_prompt[:Config.MAX_PROMPT_LENGTH]
    
    if image:
        # Use Veo 3 Fast model for image-to-video
        # Use a pre-prompt that instructs the model to study the image
        prompt = Config.IMAGE_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        output = replicate.run(
            "google-deepmind/veo-3-fast",
            input={
                "prompt": prompt,
                "image": image,
                "audio": False,  # No audio needed for GIF conversion
                "resolution": resolution
            }
        )
    else:
        # Use Sora 2 model for text-to-video
        # Format prompt using template from config
        full_prompt = Config.PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        # Request 3 seconds of video (pricing is per second, not frames)
        # Let the model use its optimal frame rate
        output = replicate.run(
            "openai/sora-2",
            input={
                "prompt": full_prompt,
                "duration": Config.GIF_DURATION,  # Request 3 seconds directly
                "audio": False,  # No audio needed for GIF conversion
                "resolution": resolution
            }
        )
    
    return output

def generate_video_cheap(user_prompt, image=None):
    # Set Replicate API token from config
    os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
    
    # Get resolution from config
    resolution = Config.RESOLUTION_MAP[Config.RESOLUTION_QUALITY]
    
    # Truncate prompt if it exceeds max length
    if len(user_prompt) > Config.MAX_PROMPT_LENGTH:
        user_prompt = user_prompt[:Config.MAX_PROMPT_LENGTH]
    
    
    if image:
        # Image-to-video with SeedAnce-1-Lite
        prompt = Config.IMAGE_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        output = replicate.run(
            "bytedance/seedance-1-lite",
            input={
                "prompt": prompt,
                "image": image,
                "resolution": resolution
            }
        )
    else:
        # Text-to-video with SeedAnce-1-Lite
        full_prompt = Config.PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        output = replicate.run(
            "bytedance/seedance-1-lite",
            input={
                "prompt": full_prompt,
                "resolution": resolution
            }
        )
    
    return output
