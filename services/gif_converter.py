from moviepy import *
from pathlib import Path

def gif_conversion(video_path):

    output_name = "output.gif"
    output_folder = "output_folder"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    # load the file and makes a snippet of it 
    clip = VideoFileClip(video_path)

    # Gets only the first 3 seconds
    clip = clip.subclipped(0,3)
    
    # Construct
    output_path = Path(output_folder) , "/" , output_name

    # Write GIF to disk
    clip.write_gif(str(output_path))
