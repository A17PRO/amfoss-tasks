import discord
from discord.ext import commands
import random
import database

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx, choice): #rock paper scissors game
        choices = ["rock", "paper", "scissors"]
        player_choice = choice.lower()
        if player_choice not in choices:
            await ctx.send("Bruh choose rock, paper, or scissors")
            return
        user = await database.get_user(ctx.author.id, ctx.author.name)
        balance = user[0]
        wager = 50
        if balance < wager:
            await ctx.send(f"U need at least {wager} berries to duel")
            return
        bot_choice = random.choice(choices)
        if player_choice == bot_choice:
            await ctx.send(f"I also picked {bot_choice}. we tied.")
            return
        #rules for the game 
        winning_choices = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if winning_choices[player_choice] == bot_choice:
            await database.update_balance(ctx.author.id, wager)
            message = f"I picked {bot_choice}. U actually won **{wager} Berries**."
        else:
            await database.update_balance(ctx.author.id, -wager)
            message = f"I picked {bot_choice}. get wrecked u lost **{wager} Berries**."
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Games(bot))