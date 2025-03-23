import os
import asyncio
from dotenv import load_dotenv
import discord 
from discord.ext import commands 

# Load .env variables
load_dotenv()
discord_token = os.getenv("discord_token")
guild_id = int(os.getenv("guild_id"))

# Enable all intents
intents = discord.Intents.all()
intents.message_content = True  # Required for message-based commands

# Setup bot with prefix commands
bot = commands.Bot(command_prefix="!", intents=intents)

# Command to load a cog dynamically
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")

# Command to unload a cog dynamically
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Syncs slash commands
    print(f"✅ Logged in as {bot.user} and synced commands!")

# Main async function to load cogs and run the bot
async def main():
    async with bot:
        await bot.load_extension("cogs.moderation")  # Auto-load the moderation cog
        await bot.start(discord_token)

# Run the bot properly with asyncio
asyncio.run(main())