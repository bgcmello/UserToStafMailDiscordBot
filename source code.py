import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
STAFF_CHANNEL_ID = 124567890987  # Replace with your staff channel ID

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="sendadmin", description="Send a message directly to the staff team")
async def sendadmin(interaction: discord.Interaction, message: str):
    channel = bot.get_channel(STAFF_CHANNEL_ID)
    if channel:
        await channel.send(f"📥 **{interaction.user}** (`{interaction.user.id}`): {message}")
        await interaction.response.send_message("✅ Your message has been sent to the admins!", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Staff channel configuration error.", ephemeral=True)

@bot.tree.command(name="reply", description="Reply to a user via direct message")
@app_commands.checks.has_permissions(manage_messages=True)  # Only users with 'Manage Messages' can run this
async def reply(interaction: discord.Interaction, user_id: str, message: str):
    # Ensure staff are only using this inside the private staff channel
    if interaction.channel.id != STAFF_CHANNEL_ID:
        await interaction.response.send_message("❌ You can only use this command in the staff channel!", ephemeral=True)
        return

    try:
        user = await bot.fetch_user(int(user_id))
        await user.send(f"💬 **Admin Reply:** {message}")
        await interaction.response.send_message(f"Reply sent to {user}!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to send DM: {e}", ephemeral=True)

bot.run("Your discord bot token")