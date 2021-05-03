import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"{round(self.bot.latency, 2)} ms")


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
