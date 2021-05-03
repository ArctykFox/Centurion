import discord
from discord.ext import commands
import requests
from core.Coin import Coin


class Crypto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.currency = "usd"
        self.supported_currencies = []
        self.last_used_coin = "bitcoin"  # DEFAULT COIN

    def get_supported_currencies(self):
        url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
        res = requests.get(url).json()
        self.supported_currencies = res

    @commands.command()
    async def price(self, ctx, coin=None):
        if coin is not None:
            self.last_used_coin = coin
            coin = Coin(coin, self.currency)
        else:
            coin = Coin(self.last_used_coin, self.currency)
        coin.get_price()
        title = f"1 {coin.name} = {coin.price} {self.currency.upper()}"
        color = 0xff0000
        embed = discord.Embed(
            title=title, color=color)

        await ctx.send(embed=embed)

    @commands.command()
    async def currency(self, ctx, currency):

        if len(self.supported_currencies) > 0:
            pass
        else:
            self.get_supported_currencies()

        if currency in self.supported_currencies:
            self.currency = currency
            await ctx.send(f"Currency changed to ``{currency.upper()}``")
        else:
            await ctx.send("Currency not supported")

    @commands.command()
    async def chart(self, ctx, coin=None):
        if coin is not None:
            self.last_used_coin = coin
            coin = Coin(coin, self.currency)
        else:
            coin = Coin(self.last_used_coin, self.currency)
        coin.get_historical_data()
        coin.generate_chart()
        await ctx.send(file=discord.File('./src/img/chart.png'))


def setup(bot: commands.Bot):
    bot.add_cog(Crypto(bot))
