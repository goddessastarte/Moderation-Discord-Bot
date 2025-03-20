import os 
from dotenv import load_dotenv
import discord 
from discord.ext import commands 

# load .env variables
load_dotenv()
discord_token = os.getenv("discord_token")

# enable all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# run the bot
bot.run(discord_token)