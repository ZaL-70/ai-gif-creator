from moviepy.editor import *


def gif_conversion():
    # load the file and makes a snippet of it 
    clip = VideoFileClip(r"C:\Users\aryan\projects\coding\ai-gif-creator\temp\Video\thorsten.mp4")

    # Gets only the first 3 seconds
    clip = clip.subclip(0,3)

    #save video clip as a gif
    clip.write_gif("gfg_gif.gif")

    clip.ipython_display()
gif_conversion()


