import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = bot.get_channel(
            659251677865443358)  # FREE FOR ALL CHANNEL

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Plebian")
        await member.add_roles(role, reason=None, atomic=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.channel.send(f'{member.display_name} has left')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            await self.channel.send(f"{after.mention} just changed his name!")

    """
    TODO: 
    -WORK ON on_member_update()
    """


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
