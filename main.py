import asyncio

import discord
from discord.ext import commands
from cogwatch import watch

from help import Help


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=Help())
        self.add_check(self.block_bots)

    @watch(path='cogs')
    async def on_ready(self):
        print('Bot ready.')
        self.load_extension("cogs.blender")
        self.load_extension("cogs.button")
        print("Cogs loaded.")

    async def block_bots(self, ctx):
        """Don't accept commands from bot accounts"""
        await self.wait_until_ready()
        return ctx.author.bot is not None


async def main():
    bot = MyBot()
    await bot.start('NjY2ODMwNjQ5NDQ0OTI1NDUw.Xh54bw.ItuceYhQ3lvz6vEnqwAn3mbL0a4')

if __name__ == '__main__':
    asyncio.run(main())
