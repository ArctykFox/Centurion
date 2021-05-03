import discord
from discord.ext import commands
import random
import json


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix


    @commands.command()
    async def ban(self, ctx, *arg):
        if ctx.message.author.permissions_in(ctx.message.channel).ban_members:
            reason = " ".join(arg[1:])
            banned_users = ctx.message.mentions
            for banned_user in banned_users:
                if banned_user == self.bot.user:
                    await ctx.send("<:bredfec:725779939131129917>")
                else:
                    if ctx.message.author.top_role.position > banned_user.top_role.position:
                        await ctx.send(f"Easy ban have fun {banned_user.display_name}")
                        await banned_user.ban(reason=reason)
                    else:
                        await ctx.send(f"You cant ban {banned_user.mention}")
        else:
            await ctx.send("You dont have permission to ban")

    @commands.command()
    async def kick(self, ctx):
        if ctx.message.author.permissions_in(ctx.message.channel).kick_members:
            kicked_users = ctx.message.mentions

            for kicked_user in kicked_users:
                if kicked_user == self.bot.user:
                    await ctx.send("<:bredfec:725779939131129917>")
                else:
                    if ctx.message.author.top_role.position > kicked_user.top_role.position:
                        await ctx.send(f"Easy kick have fun {kicked_user.display_name}")
                        await kicked_user.kick()
                    else:
                        await ctx.send(f"You cant kick {kicked_user.mention}")
        else:
            await ctx.send("<:bredfec:725779939131129917>")

    @commands.command()
    async def mute(self, ctx, *args):
        muted_users = ctx.message.mentions

        for muted_user in muted_users:
            if muted_user == self.bot.user:
                await ctx.send("<:harold:718791729398022184>")

            if ctx.message.author.top_role.position > muted_user.top_role.position and ctx.message.author.permissions_in(ctx.message.channel).manage_roles:
                guild_roles = await ctx.guild.fetch_roles()
                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

                if muted_role in guild_roles:
                    pass
                else:
                    await ctx.guild.create_role(name="Muted")

                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
                muted_user_roles = muted_user.roles[1:]

                for role in muted_user_roles:
                    await muted_user.remove_roles(role, reason=None, atomic=True)

                await muted_user.add_roles(muted_role, reason=None, atomic=True)
                await ctx.send(f"Easy mute have fun {muted_user.mention}")
            else:
                await ctx.send("<:bredfec:725779939131129917>")

    @commands.command()
    async def unmute(self, ctx):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_roles:
            muted_users = ctx.message.mentions

            for muted_user in muted_users:
                if muted_user == self.bot.user:
                    pass

                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

                if muted_role in muted_user.roles:
                    await muted_user.remove_roles(muted_role, reason=None, atomic=True)
                    await ctx.send(f"{muted_user.mention} has been unmuted!")

                    if ctx.guild.id == 659188268029444110:
                        plebian_role = discord.utils.get(
                            ctx.guild.roles, name="Plebian")
                        await muted_user.add_roles(plebian_role, reason=None, atomic=True)
                else:
                    await ctx.send(f"{muted_user.mention} needs to be muted first!")
        else:
            await ctx.send("<:bredfec:725779939131129917>")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx):
        members = ctx.message.mentions
        roles = ctx.message.role_mentions

        for member in members:
            if ctx.message.author.top_role.position >= member.top_role.position:
                for role in roles:
                    await member.add_roles(role, reason=None, atomic=True)
                    await ctx.send(f"{member.display_name} got {role}")
            else:
                await ctx.send(f"You cant change role for {member.mention}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx):
        members = ctx.message.mentions
        roles = ctx.message.role_mentions

        for member in members:
            if ctx.message.author.top_role.position >= member.top_role.position:
                for role in roles:
                    await member.remove_roles(role, reason=None, atomic=True)
                    await ctx.send(f"{member.display_name} lost {role}")
            else:
                await ctx.send(f"You cant change role for {member.mention}")

    @commands.command()
    async def chill(self, ctx, arg):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_channels:
            await ctx.channel.edit(slowmode_delay=int(arg))
            if int(arg) == 0:
                await ctx.send("Cooldown has been disabled!")
            else:
                await ctx.send("Cooldown has been enabled!")
        else:
            await ctx.send("<:bredfec:725779939131129917>")

    @commands.command()
    async def dlt(self, ctx, arg):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
            await ctx.message.channel.purge(limit=int(arg))
        else:
            await ctx.send("You cant delete messages")

    @commands.command()
    async def prefix(self, ctx, prefix):
        self.bot.command_prefix = prefix
        await ctx.send(f"Prefix changed to ``{prefix}``")


def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))
