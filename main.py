import asyncio
from configparser import ConfigParser

import discord
from discord.ext import commands
from cogwatch import watch

from help import Help


def read_config():
    config = ConfigParser()
    config.read('config.ini')
    return config['Bot']


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=Help())
        self.add_check(self.global_check)

    @watch(path='cogs')
    async def on_ready(self):
        print('Bot ready.')

        # Load any other cogs you may have here
        self.load_extension("cogs.blender")
        self.load_extension("cogs.button")
        print("Cogs loaded.")

    async def global_check(self, ctx):
        await self.wait_until_ready()
        return ctx.author.bot is not None


async def main():
    bot = MyBot()
    await bot.start(read_config()['token'])

if __name__ == '__main__':
    asyncio.run(main())
