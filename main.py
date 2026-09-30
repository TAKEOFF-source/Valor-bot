import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"BOT ONLINE: {bot.user} - VALOR ready!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # 30 Aug se results check
    if message.channel.name == "results":
        print(f"New result: {message.content} by {message.author}")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
