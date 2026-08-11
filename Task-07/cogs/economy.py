import discord
from discord.ext import commands
import time
import random
import database

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bounty(self, ctx): #shows berries
        user = await database.get_user(ctx.author.id, ctx.author.name)
        await ctx.send(f"Hey {ctx.author.name}, u have **{user[0]} Berries**.")

    @commands.command()
    async def setsail(self, ctx): #gets the daily reward
        user = await database.get_user(ctx.author.id, ctx.author.name)
        current_time = time.time()
        #sets a cooldown of 24 hours
        if current_time - user[1] < 86400:
            hours_left = int((86400 - (current_time - user[1])) / 3600)
            await ctx.send(f"Chill man, u gotta wait {hours_left} hours")
            return
        await database.update_balance(ctx.author.id, 500)
        await database.update_cooldown(ctx.author.id, "last_daily", current_time)
        await ctx.send("W. u successfully raided a ship and got **500 Berries**.")

    @commands.command()
    async def trade(self, ctx, member: discord.Member, amount): #trades with another user
        try:
            amount = int(amount)
        except ValueError:
            await ctx.send("Bro enter a real number for the amount")
            return
        if amount <= 0:
            await ctx.send("HAHA no negative numbers")
            return
        sender = await database.get_user(ctx.author.id, ctx.author.name)
        if sender[0] < amount:
            await ctx.send("Sorry but ur too broke")
            return
        #get the target user
        await database.get_user(member.id, member.name)
        await database.update_balance(ctx.author.id, -amount)
        await database.update_balance(member.id, amount)
        await ctx.send(f"Done. {ctx.author.name} sent **{amount} Berries** over to {member.name}.")

    @commands.command()
    async def raid(self, ctx, member: discord.Member): #robs users
        if ctx.author.id == member.id:
            await ctx.send("U tried to raid urself, Really?")
            return
        attacker = await database.get_user(ctx.author.id, ctx.author.name)
        target = await database.get_user(member.id, member.name)
        current_time = time.time()
        #sets a cooldown of 1 hour 
        if current_time - attacker[2] < 3600:
            await ctx.send("Marines are suspicious, wait an hour")
            return
        if target[0] < 50:
            await ctx.send(f"Leave {member.name} alone, they literally have nothing")
            return
        await database.update_cooldown(ctx.author.id, "last_rob", current_time)
        #50% chance to steal 
        if random.random() > 0.5:
            stolen = int(target[0] * 0.2)
            await database.update_balance(ctx.author.id, stolen)
            await database.update_balance(member.id, -stolen)
            await ctx.send(f"LFG!! u jumped {member.name} and took **{stolen} Berries**!")
        else:
            lost = int(attacker[0] * 0.1)
            await database.update_balance(ctx.author.id, -lost)
            await ctx.send(f"RIP u got caught lacking by {member.name}. u dropped **{lost} Berries** running away.")

    @commands.command()
    async def worstgeneration(self, ctx): #shows leaderboard
        top_users = await database.get_top_users(5)
        board = "**The Worst Generation**\n"
        for number, (username, balance) in enumerate(top_users, 1):
            board += f"{number}. **{username}** - {balance} Berries\n"
        await ctx.send(board)

async def setup(bot): 
    await bot.add_cog(Economy(bot))