import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from pathlib import Path
import database

load_dotenv()
TOKEN = os.getenv("discord_token")

class BerryBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await database.setup_db()
        cogs_folder = Path("./cogs")
        for file in cogs_folder.glob("*.py"):
            await self.load_extension(f"cogs.{file.stem}")

bot = BerryBot()

@bot.event
async def on_ready():
    print("Berry Broker is online") #init the bot

if TOKEN:
    bot.run(TOKEN)