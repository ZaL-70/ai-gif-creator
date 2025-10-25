import os
import discord
from config import Config
from dotenv import load_dotenv
from utils.helpers import validate_prompt
from services.gif_converter import *
from services.ai_generator import *
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(Config.COMMAND_PREFIX):
        return
    
    content = message.content[len(Config.COMMAND_PREFIX):].strip()
    #Command
    if content.lower().startswith('gif '):
        prompt = content[4:].strip()
        
        # Validate
        is_valid, error = validate_prompt(prompt)
        if not is_valid:
            await message.channel.send(f"error caused {error}")
            return
            
        status_msg = await message.channel.send("Generating the gif... (1-2 minutes)")    
        
        try:
            # Generates video 
            loop = asyncio.get_event_loop()
            vid_output = await loop.run_in_executor(None, generate_video, prompt)
            
            if isinstance(vid_output, list):
                video_url = vid_output[0]
            else:
                video_url = vid_output
            
            await status_msg.edit(content="Converting to GIF...")
            
            # Converts to gif
            gif_path = await loop.run_in_executor(
                None,
                download,
                video_url
            )
            
            # Checks file size
            file_size_mb = os.path.getsize(gif_path) / (1024 * 1024)
            if file_size_mb > Config.MAX_FILE_SIZE_MB:
                await status_msg.edit(content=f"Error: GIF too large: {file_size_mb:.1f}MB (max {Config.MAX_FILE_SIZE_MB}MB)")
                os.unlink(gif_path)
                return
            
            # Send GIF 
            await message.channel.send(file=discord.File(gif_path))
            await status_msg.delete()
            
            # Clean the GIF file 
            os.unlink(gif_path)
        
        except Exception as e:
            await status_msg.edit(content=f"Error: {str(e)}")
            print(f"Error generating GIF: {e}")
            import traceback
            traceback.print_exc()
        
if __name__ == '__main__':
    client.run(Config.DISCORD_TOKEN)    