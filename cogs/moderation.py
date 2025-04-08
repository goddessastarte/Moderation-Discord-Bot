from dotenv import load_dotenv
import discord 
import os
from discord import app_commands
from discord.ext import commands


load_dotenv()
GUILD_ID = int(os.getenv('GUILD_ID'))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="kick a member from the server0")
    @app_commands.describe(member="The member to kick", reason="Reason for the kick")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You don't have permission to kick a member", ephemeral=True)
            return
        
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.mention} has been kicked.")
        except discord.Forbidden:
            await interaction.response.send_message("I can't kick that user. Check my role permissions.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occured: {e}", ephemeral=True)
        await self.log_action(interaction, "Kick", member, reason)

    @app_commands.command(name="ban", description="ban a member from the server")
    @app_commands.describe(member="The member to ban", reason="Reason for the ban")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You don't have permission to ban a member", ephemeral=True)
            return
        print("Loaded ban command successfully")
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.mention} has been banned.")
        except discord.Forbidden:
            await interaction.response.send_message("I can't ban that user. check my role permissions.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"An error occured: {e}", ephemeral=True)
        await self.log_action(interaction, "Ban", member, reason)

    @app_commands.command(name="warn", description="Privately warn a member via DM")
    @app_commands.describe(member="The member to warn", reason="Reason for the warning")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You don't have permission to warn members.", ephemeral=True)
            return

        try:
            await member.send(f"⚠️ You have been warned in **{interaction.guild.name}** for: {reason}")
            await interaction.response.send_message(f"{member.mention} has been warned via DM ✅", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Couldn't DM the user. They might have DMs disabled.", ephemeral=True)
        await self.log_action(interaction, "Warn", member, reason)

    @app_commands.command(name="clear", description="Delete a number of recent messages")
    @app_commands.describe(amount="Number of messages to delete")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "You don't have permission to delete messages.",
                ephemeral=True
            )
            return

        if not interaction.response.is_done():  # ✅ only defer if we haven’t already
            await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount + 1)

        await interaction.followup.send(
            f"🧹 Deleted {len(deleted)-1} messages.",
            ephemeral=True,
            delete_after=3
        )

        await self.log_action(interaction, "Clear", interaction.user, f"Deleted {amount} messages")



    async def log_action(self, interaction, action_type, target: discord.Member, reason: str):
        log_channel = discord.utils.get(interaction.guild.text_channels, name="mod-log")
        if not log_channel:
            return 
        
        embed = discord.Embed(
            title="f{action_type} Logged",
            description=f"**Target:** {target.mention}\n**Moderator:** {interaction.user.mention}\n**Reason** {reason}",
            color=discord.color.orange()
        )
        embed.set_footer(text=f"Time: {interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))