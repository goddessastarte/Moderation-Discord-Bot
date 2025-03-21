import os 
from dotenv import load_dotenv
import discord 
from discord.ext import commands 

# load .env variables
load_dotenv()
discord_token = os.getenv("discord_token")
guild_id = int(os.getenv("guild_id"))
# enable all intents
intents = discord.Intents.all()

# setup bot with prefix commands
bot = commands.Bot(command_prefix="!", intents=intents)

# add a simple !hello command
@bot.command()
async def hello(ctx):
    """responds with a greeting"""
    await ctx.send("Hello <3 !")

# add a simple /hello command
@bot.tree.command(name="hello", description="say hello!")
async def slash_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Haiiii <3 !!!")

# add a /ping command 
@bot.tree.command(name="ping",description="ping pong")
async def pingpong(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

# add a /info command 
@bot.tree.command(name="info", description="give info about the bot")
async def infobot(interaction : discord.Interaction):
    #app_info = bot.application.owner
    await interaction.response.send_message(f"{bot.application.owner} {bot.user} {bot.activity} {bot.status}")

# add a /say command
@bot.tree.command(name="say", description="repeats the message the user gives")
@discord.app_commands.describe(message="The message you want the bot to repeat")
async def say(interaction: discord.Interaction, message:str):
    await interaction.response.send_message(message)

# register and update slash commands with discord
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} and synced commands!")

# run the bot
bot.run(discord_token)