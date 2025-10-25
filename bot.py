import os
import discord
from config import Config
from dotenv import load_dotenv
from utils.helpers import validate_prompt
from services.gif_converter import *
from services.ai_generator import *
import asyncio
import datetime
import json

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
    # Command
    if content.lower().startswith('gif '):
        prompt = content[4:].strip()

        use_recent = prompt.startswith("-recent")
        use_expensive = "-expensive" in prompt
        context_messages = None

        if use_recent:
            prompt = prompt.replace("-recent", "", 1).strip()
        if use_expensive:
            prompt = prompt.replace("-expensive", "").strip()
            
        if use_recent:
            messages = []
            async for msg in message.channel.history(limit=10):
                if msg.author.bot:
                    continue  # skip bots
                messages.append({
                    "author": str(msg.author),
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat(),
                })
            messages.reverse()  # chronological order

            os.makedirs("data", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join("data", f"messages_{timestamp}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            # Format context messages for prompt with author, timestamp, and content
            context_messages = "\n".join([
                f"- [{msg['timestamp']}] {msg['author']}: {msg['content']}" 
                for msg in messages[-5:]
            ])  # Last 5 messages

        # Check if image prompt
        image_url = None
        if message.attachments:
            attachment = message.attachments[0]
            
            if attachment.content_type and attachment.content_type.startswith('image/'):
                if attachment.size > 8 * 1024 * 1024:
                    await message.channel.sent("Error: Image is too large! Max size is 8MB.")
                    return
                image_url = attachment.url
                print(f"image detected:", {image_url})
            else:
                await message.channel.send("Incorrect image type.")
                return    
        
        # Validate
        is_valid, error = validate_prompt(prompt)
        if not is_valid:
            await message.channel.send(f"error caused {error}")
            return
            
        if image_url:
            status_msg = await message.channel.send("Creating gif from Image + Prompt... (1-2 minutes)")
        else:
            status_msg = await message.channel.send("Generating the gif... (1-2 minutes)")

        try:
            # Generates video 
            loop = asyncio.get_event_loop()
            
            # Choose model based on -expensive flag
            generator_func = generate_video if use_expensive else generate_video_cheap
            
            # Build kwargs
            kwargs = {"image": image_url}
            if use_recent and context_messages:
                kwargs["context"] = context_messages
            
            vid_output = await loop.run_in_executor(
                None,
                lambda: generator_func(prompt, **kwargs)
            )
            
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
            await message.channel.send(content=f"✨ Here's your GIF: *{prompt}*", file=discord.File(gif_path))
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
