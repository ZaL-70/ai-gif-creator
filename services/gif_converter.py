import os
from moviepy import *
import requests
import tempfile
from pathlib import Path
from config import Config

def gif_conversion(video_path):
    output_name = "output.gif"
    output_folder = "output_folder"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Load the video
    clip = VideoFileClip(video_path)

    # Gets only the first 3 seconds
    clip = clip.subclipped(0, Config.GIF_DURATION)
    
    # Get resolution from config (e.g., "480p" -> 480)
    resolution_str = Config.RESOLUTION_MAP[Config.RESOLUTION_QUALITY]
    target_height = int(resolution_str.replace('p', ''))
    
    # Resize to match config resolution while maintaining aspect ratio
    clip = clip.resized(height=target_height)
    
    # Construct output path
    output_path = Path(output_folder) / output_name
 
    # Write GIF to disk with optimized settings from config
    clip.write_gif(
        str(output_path),
        fps=Config.GIF_FPS  # Use FPS from config (10 fps)
    )

    clip.close()

    return output_path

def download(video_url):
    try:
        # Download video
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()

        # Save to temp file
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4', dir=Config.TEMP_DIR)
        temp_video.write(response.content)
        temp_video.close()

        # Convert to GIF
        gif_path = gif_conversion(temp_video.name)

        # Clean up video file
        os.unlink(temp_video.name)

        return gif_path

    except Exception as e:
        raise Exception(f"GIF conversion failed: {str(e)}")
