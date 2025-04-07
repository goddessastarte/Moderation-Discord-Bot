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
    """
    on_ready : which handles the event when
    the Client has established a connection to Discord 
    """
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} has connected to Discord!\n'
        f'{guild.name}(id: {guild.id})'
        )


@bot.event 
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send( # private message member
        f'Hi {member.name}, welcome to my discord server'
    )


@bot.event 
async def on_message(message):
    if message.author == bot.user:
        return
    
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji',
        'Bingpot!',
        (
            'cool. cool cool cool cool cool cool,'
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    await bot.process_commands(message)

    
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event 
async def on_command_error(ctx, error):
    print(f"Error: {error}")
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for the command')


bot.run(TOKEN)