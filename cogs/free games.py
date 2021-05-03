import discord
from discord.ext import commands
from core.Game import Game
import asyncio
import requests
from bs4 import BeautifulSoup as bs


class Track(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.is_tracking = False
        self.games = []
        self.game_titles = []
        self.delay = 3600 * 6  # 6 HOURS

    def get_games(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0"}
        url = "https://gamesfree.today/"
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "lxml")

        games = [x for x in soup.find_all("div", class_="game")]
        for game in games:
            name = game.find_all("div", class_="description-part")[0].h3.text
            description = game.find_all(
                "div", class_="description-part")[0].span.text
            link = game.find_all("div", class_="send-off-part")[0].a["href"]
            image = game.find_all(
                "div", class_="image-part")[0].img["data-src"]

            game_object = Game(name, description, link, image)

            if game_object.name in self.game_titles:
                pass
            else:
                self.game_titles.append(game_object.name)
                self.games.append(game_object)

    @commands.command()
    async def track(self, ctx):
        if not self.is_tracking:
            self.is_tracking = True

            games_channel = discord.utils.get(
                ctx.guild.channels, name="free-games")

            if games_channel is None:
                guild = ctx.guild
                games_channel = await guild.create_text_channel('free-games')
            else:
                games_channel = discord.utils.get(
                    ctx.guild.channels, name="free-games")

            guild_roles = await ctx.guild.fetch_roles()
            games_role = discord.utils.get(ctx.guild.roles, name="Free Games")

            if games_role in guild_roles:
                pass
            else:
                await ctx.guild.create_role(name="Free Games")

            games_role = discord.utils.get(ctx.guild.roles, name="Free Games")

            await ctx.send("Tracking Games!")

            while self.is_tracking:
                self.get_games()

                for game in self.games:
                    title = game.name
                    image = game.image
                    description = f"{game.description}\nlink : {game.link}"
                    color = 0xff0000

                    embed = discord.Embed(
                        title=title, image=image, description=description, color=color)
                    embed.set_image(url=game.image)

                    await games_channel.send(embed=embed)
                    await games_channel.send(f"{games_role.mention}")

                #CLEAR THE GAMES LIST
                self.games = []

                await asyncio.sleep(self.delay)
        else:
            await ctx.send("Already tracking Games!")


def setup(bot: commands.bot):
    bot.add_cog(Track(bot))
