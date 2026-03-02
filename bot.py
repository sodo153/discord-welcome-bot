import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is None:
        return

    embed = discord.Embed(
        title="🎉 Welcome!",
        description=f"**Welcome {member.mention} ברוך הבא לשרת של סיקסון**",
        color=discord.Color.gold()
    )

    embed.set_image(url=member.display_avatar.url)
    await channel.send(embed=embed)

@bot.tree.command(name="servermessage", description="Owner only: send big message to all channels")
@app_commands.describe(message="Message to send")
async def servermessage(interaction, message: str):

    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message(
            "❌ Only the server owner can use this command.",
            ephemeral=True
        )
        return

    await interaction.response.send_message("✅ Sending message...", ephemeral=True)

    big_message = f"# **{message}**"

    for channel in interaction.guild.text_channels:
        try:
            await channel.send(big_message)
        except:
            pass

bot.run(TOKEN)
