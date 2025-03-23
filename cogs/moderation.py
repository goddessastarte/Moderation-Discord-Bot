from discord.ext import commands

# Define a Cog class for moderation commands
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Store the bot instance

    # Prefix command: !ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")  # Replies with "Pong!" when you type !ping

# Required async setup function to load the Cog
async def setup(bot):
    await bot.add_cog(Moderation(bot))  # Add the cog to the bot