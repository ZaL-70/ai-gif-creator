import replicate
import os
from config import Config

def generate_video(user_prompt, images=None, resolution_quality="low"):
    # Set Replicate API token from config
    os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
    
    # Get resolution from config based on quality parameter
    resolution = Config.RESOLUTION_MAP[resolution_quality]
    
    if images:
        prompt = Config.IMAGE_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        # Handle single or multiple images
        if isinstance(images, list):
            if len(images) == 1:
                # Use Veo 3 Fast for single image - requires specific settings
                input_params = {
                    "prompt": prompt,
                    "image": images[0],
                    "resolution": "720p",  # Veo only supports 720p or 1080p
                    "duration": 4  # Veo only supports 4, 6, or 8 seconds
                }
                output = replicate.run(
                    "google/veo-3-fast",
                    input=input_params
                )
            else:
                # Use Seedance-1-Lite with reference_images for multiple images
                input_params = {
                    "prompt": prompt,
                    "resolution": resolution,
                    "duration": Config.GIF_DURATION,
                    "reference_images": images
                }
                output = replicate.run(
                    "bytedance/seedance-1-lite",
                    input=input_params
                )
        else:
            # Single image (not in list) - use Veo 3 Fast
            input_params = {
                "prompt": prompt,
                "image": images,
                "resolution": "720p",  # Veo only supports 720p or 1080p
                "duration": 4  # Veo only supports 4, 6, or 8 seconds
            }
            output = replicate.run(
                "google/veo-3-fast",
                input=input_params
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

def generate_video_cheap(user_prompt, images=None, resolution_quality="low"):
    # Set Replicate API token from config
    os.environ["REPLICATE_API_TOKEN"] = Config.REPLICATE_API_TOKEN
    
    # Get resolution from config based on quality parameter
    resolution = Config.RESOLUTION_MAP[resolution_quality]
    
    if images:
        prompt = Config.IMAGE_PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        
        # Handle single or multiple images
        if isinstance(images, list):
            if len(images) == 1:
                # Use Veo 3 Fast for single image - requires specific settings
                input_params = {
                    "prompt": prompt,
                    "image": images[0],
                    "resolution": "720p",  # Veo only supports 720p or 1080p
                    "duration": 4  # Veo only supports 4, 6, or 8 seconds
                }
                output = replicate.run(
                    "google/veo-3-fast",
                    input=input_params
                )
            else:
                # Use Seedance-1-Lite with reference_images for multiple images
                input_params = {
                    "prompt": prompt,
                    "resolution": resolution,
                    "duration": Config.GIF_DURATION,
                    "reference_images": images
                }
                output = replicate.run(
                    "bytedance/seedance-1-lite",
                    input=input_params
                )
        else:
            # Single image (not in list) - use Veo 3 Fast
            input_params = {
                "prompt": prompt,
                "image": images,
                "resolution": "720p",  # Veo only supports 720p or 1080p
                "duration": 4  # Veo only supports 4, 6, or 8 seconds
            }
            output = replicate.run(
                "google/veo-3-fast",
                input=input_params
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
