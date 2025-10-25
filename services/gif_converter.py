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
    # load the file and makes a snippet of it 
    clip = VideoFileClip(video_path)

    # Gets only the first 3 seconds
    clip = clip.subclipped(0,3)
    
    # Construct
    output_path = Path(output_folder) / output_name
 
    # Write GIF to disk
    clip.write_gif(str(output_path))

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

gif_conversion(r"C:\Users\aryan\projects\coding\ai-gif-creator\temp\Video\thorsten.mp4")