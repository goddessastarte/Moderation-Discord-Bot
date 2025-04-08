import os
import random 

import discord 
from discord.ext import commands 
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online.")
    synced = await bot.tree.sync()  # global sync
    print(f"✅ Synced {len(synced)} global commands")

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.moderation")
bot.run(TOKEN)