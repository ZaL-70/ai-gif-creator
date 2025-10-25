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
    
    output = replicate.run("anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                        input={"prompt": full_prompt,
                               "num_frames": frames})
    return output
