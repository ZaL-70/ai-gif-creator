from moviepy import *
from pathlib import Path


def gif_conversion():
    
    Path("temp/GIF").mkdir(parents=True, exist_ok=True)
    output_name = "output.gif"
    # load the file and makes a snippet of it 
    clip = VideoFileClip(r"C:\Users\aryan\projects\coding\ai-gif-creator\temp\Video\thorsten.mp4")

    # Gets only the first 3 seconds
    clip = clip.subclipped(0,3)

    #save video clip as a gif
    clip.write_gif("gfg_gif.gif")
    
        # Construc
    output_path = Path(output_folder) / output_name

    # Write GIF to disk
    clip.write_gif(str(output_path))



