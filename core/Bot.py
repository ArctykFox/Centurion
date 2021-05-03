import discord
import os
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=".", intents=intents)
        self.bot_activity = "THE GLORY OF ROME"
        # create the background task and run it in the background
        # self.bg_task = self.loop.create_task(self.track_crypto())

    # LOOP OVER THE COGS AND LOAD THEM
    def load_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Cog loaded : {filename[:-3].upper()}")

    # EVENTS
    async def on_ready(self):
        print('---------------------------------')
        self.load_cogs()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot_activity))
        # IF THIS EXECUTES THEN EVERYTHING LOADED PROPERLY
        print('---------------------------------')
        print(f'Logged in as : {self.user.name}')
        print(f"Bot ID       : {self.user.id}")
        print('---------------------------------')
        for guild in self.guilds:
            print(f"connected to {guild}")
        print('---------------------------------')

    def init(self, token):
        self.run(token)
