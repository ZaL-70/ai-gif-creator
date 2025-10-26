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
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

user_cooldowns = {}
COOLDOWN_SECONDS = 60

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
    
    # Create help command
    if content.lower() == 'help':
        help_embed = discord.Embed(
            title = " GIF Goblin 🧌",
            description = "Generate custom GIFs using AI. Here are the steps:",
            colour=0x9caa58 
        )
        
        help_embed.add_field(
            name="Text to GIF",
            value="```!gif <your prompt>```\nExample: `!gif dancing robot in space`",
            inline=False
        )
        
        help_embed.add_field(
            name="Image to GIF",
            value="Upload 1 or more images + `!gif <prompt>`\nExample: Upload photo + `!gif waving hello`",
            inline=False
        )
        
        help_embed.add_field(
            name="Flags & Options",
            value=(
                "`-resolution low/medium/high` - Set quality (default: low)\n"
                "`-expensive` - Use premium model for better results\n"
                "`-recent` - Include last 10 messages as context"
            ),
            inline=False
        )
    
        help_embed.add_field(
            name="Example Commands",
            value=(
                "`!gif cat playing piano`\n"
                "`!gif -resolution high sunset over mountains`\n"
                "`!gif -expensive cyberpunk city at night`\n"
                "`!gif -recent -resolution medium` (uses chat context)"
            ),
            inline=False
        )
        
        help_embed.set_footer(
            text="Don't get too wacky. Enjoy!"
        )
        
        await message.channel.send(embed=help_embed)
        return
    
    # Command
    if content.lower().startswith('gif '):
        prompt = content[4:].strip()

        user_id = message.author.id
        current_time = time.monotonic()

        # 1. Check cooldowns
        last = user_cooldowns.get(user_id)
        if last is not None:
            time_since_last = current_time - last
            if time_since_last < COOLDOWN_SECONDS:
                remaining = int(COOLDOWN_SECONDS - time_since_last)
                await message.channel.send(f"⏳ Please wait {remaining} seconds before generating another GIF!")
                return

        # 2. Check for flags
        use_recent = "-recent" in prompt
        use_expensive = "-expensive" in prompt
        resolution_quality = "low"  # Default to low
        
        # Resolution flag check
        if "-resolution" in prompt:
            parts = prompt.split()
            for i, part in enumerate(parts):
                if part == "-resolution" and i + 1 < len(parts):
                    next_part = parts[i + 1].lower()
                    if next_part in ["low", "medium", "high"]:
                        resolution_quality = next_part
                        # Remove both -resolution and the quality value
                        prompt = prompt.replace(f"-resolution {parts[i + 1]}", "", 1).strip()
                    break
        
        # Remove flags from prompt
        if use_recent:
            prompt = prompt.replace("-recent", "", 1).strip()
        if use_expensive:
            prompt = prompt.replace("-expensive", "", 1).strip()
        
        # Final cleanup: remove any extra spaces
        prompt = " ".join(prompt.split())
        user_prompt = prompt  # store original prompt from user before adding context to the prompt

        # Recent flag check (message context)
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
            json_string = json.dumps(messages, indent=2, ensure_ascii=False)

            os.makedirs("data", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join("data", f"messages_{timestamp}.json")

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            # Combine context and prompt
            if json_string:
                prompt = f"Here's the message history:\n{json_string}\n\nHere's the User Prompt:\n{prompt}"

        # 3. Check if image prompt - support multiple images
        image_urls = []
        if message.attachments:
            for idx, attachment in enumerate(message.attachments):
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    if attachment.size > 8 * 1024 * 1024:
                        await message.channel.send(f"Error: Image {idx+1} is too large! Max size is 8MB.")
                        return
                    image_urls.append(attachment.url)
                    print(f"Image {idx+1} detected: {attachment.url}")
                else:
                    await message.channel.send(f"Incorrect image type for attachment {idx+1}.")
                    return    
        
        # 4. Validate prompt for safety
        is_valid, error = validate_prompt(prompt)
        if not is_valid:
            await message.channel.send(f"error caused {error}")
            return
            
        if image_urls:
            num_images = len(image_urls)
            status_msg = await message.channel.send(f"Creating gif from {num_images} image(s) + Prompt... (1-2 minutes)")
        else:
            status_msg = await message.channel.send("Generating the gif... (1-2 minutes)")

        user_cooldowns[user_id] = current_time  # Set cooldown after successful prompt

        # 5. Generate the gif
        try:
            # Generates video 
            loop = asyncio.get_event_loop()
            
            # Choose model based on -expensive flag
            generator_func = generate_video if use_expensive else generate_video_cheap
            
            # Moving to the correct model
            if image_urls:
                vid_output = await loop.run_in_executor(
                    None,
                    lambda: generator_func(prompt, image_urls, resolution_quality)
                )
            else:
                vid_output = await loop.run_in_executor(
                    None,
                    lambda: generator_func(prompt, None, resolution_quality)
                )
            
            if isinstance(vid_output, list):
                video_url = vid_output[0]
            else:
                video_url = vid_output

            # Converts to gif
            await status_msg.edit(content="Converting to GIF...")
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
            await message.channel.send(content=f"✨ Here's your GIF: *{user_prompt}*", file=discord.File(gif_path))
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
