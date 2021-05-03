import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup as bs
from youtube_search import YoutubeSearch
import json


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    def get_joke(self):
        url = "https://icanhazdadjoke.com/"
        page = requests.get(url)
        soup = bs(page.content, "lxml")

        joke = soup.find('p', class_="subtitle")
        return joke.contents[0]

    @commands.command()
    async def joke(self, ctx):
        joke = self.get_joke()
        await ctx.send(joke)

    def get_fact(self):
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        res = requests.get(url).json()
        fact = res["text"]
        return fact

    @commands.command()
    async def fact(self, ctx):
        fact = self.get_fact()
        await ctx.send(fact)

    def get_pic(self, board):
        url = f"https://4chan.org/{board}/"
        page = requests.get(url)
        soup = bs(page.content, "lxml")
        res = [x["href"] for x in soup.find_all("a", class_="fileThumb")]
        try:
            url = random.choice(res)
            url = f"https:{url}"
            return url
        except:
            return f"{board} is not a valid board"

    @commands.cooldown(1, 3, type=commands.BucketType.user)
    @commands.command()
    async def chan(self, ctx, board):
        if ctx.message.channel.is_nsfw():
            url = self.get_pic(board)
            await ctx.send(url)
            # await ctx.send(file=discord.File('img.png'))
        else:
            await ctx.send(f"{ctx.message.author.mention} no")

    @commands.command()
    async def spm(self, ctx, *args):

        plebian_role = discord.utils.get(ctx.guild.roles, name="Plebian")
        can_spam = not (plebian_role in ctx.message.author.roles)

        if can_spam:
            string = " ".join(args)
            for j in range(0, (ctx.message.author.top_role.position - 7)):
                await ctx.send(string)
        else:
            await ctx.send("Plebs cant spam <:bredfec:725779939131129917>")

    def get_video(self, query):
        results = YoutubeSearch(query, max_results=10).to_dict()
        base_url = "https://www.youtube.com"
        url_suffix = [x["url_suffix"] for x in results]
        try:
            return base_url + random.choice(url_suffix)
        except:
            return f"No results for {query}"

    @commands.cooldown(1, 3, type=commands.BucketType.user)
    @commands.command()
    async def yt(self, ctx, query):
        url = self.get_video(query)
        await ctx.send(url)


def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))
