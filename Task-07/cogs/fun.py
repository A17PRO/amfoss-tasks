import discord
from discord.ext import commands
import aiohttp
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roast(self, ctx, member: discord.Member):
        flames = [
            "Bro ur broke asf, make some money",
            "Your python code makes me want to rip my eyes out",
            "I've seen iron players in valorant with better mechanics than u",
            "U look like u definitely write discord bots in java",
            "Even buggy wouldnt claim u"
        ]
        roast = random.choice(flames)
        await ctx.send(f"Hey {member.mention}, {roast}")

    @commands.command()
    async def logpose(self, ctx):
        api_url = "https://api.api-onepiece.com/v2/characters/en"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status != 200:
                        await ctx.send("Log Pose is spinning out... API returned an error.")
                        return
                    
                    data = await response.json()
                    
                    if not data or not isinstance(data, list):
                        await ctx.send("Log Pose found no data from the Grand Line.")
                        return
                    
                    # Pick a random character dynamically from the JSON response list
                    character = random.choice(data)
                    
                    # Safely extract and format fields returned by the API
                    name = character.get("name", "Unknown")
                    crew = character.get("crew", {})
                    crew_name = crew.get("name", "Independent / None") if isinstance(crew, dict) else "Independent / None"
                    
                    bounty = character.get("bounty", "Unknown")
                    status = character.get("status", "Unknown")
                    job = character.get("job", "Unknown")
                    
                    await ctx.send(
                        f"🧭 **Log Pose points to the Grand Line!**\n"
                        f"**Target:** {name}\n"
                        f"**Job/Role:** {job}\n"
                        f"**Crew:** {crew_name}\n"
                        f"**Bounty:** {bounty}\n"
                        f"**Status:** {status}"
                    )
                    
        except aiohttp.ClientError:
            await ctx.send("Connection failed. The Grand Line is experiencing heavy interference.")

async def setup(bot):
    await bot.add_cog(Fun(bot))