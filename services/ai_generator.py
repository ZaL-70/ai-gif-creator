import replicate
import os
from config import Config

def generate_video(user_prompt):
    # Set Replicate API token from config
    os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
    
    # Truncate prompt if it exceeds max length
    if len(user_prompt) > Config.MAX_PROMPT_LENGTH:
        user_prompt = user_prompt[:Config.MAX_PROMPT_LENGTH]
    
    # Format prompt using template from config
    full_prompt = Config.PROMPT_TEMPLATE.format(user_prompt=user_prompt)
    
    # Calculate frames based on GIF_DURATION and GIF_FPS from config
    frames = Config.GIF_DURATION * Config.GIF_FPS
    
    output = replicate.run("another-ai-studio/zeroscope-v2-xl",
                        input={"prompt": full_prompt,
                               "motion_bucket_id": 40, 
                               "frames": frames})
    return output
