import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

import discord
from discord.ext import commands


class DataManager:
    """A context manager class for reading and writing userdata."""
    def __init__(self):
        # Change this path to change where the scoring data for users is stored
        self.PATH = 'button_data.json'

    def __enter__(self):
        if os.path.exists(self.PATH):
            with open(self.PATH, 'r+') as file:
                self.data = json.load(file)
        else:
            self.data = {}  # if the user data hasn't been created yet, return empty dict

        # JSON does weird things with int keys, so we store then as str, then convert them back here
        self.data = defaultdict(int, {int(k): v for k, v in self.data.items()})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # convert the int keys into strings for storage
        str_data = {str(k): v for k, v in self.data.items()}

        with open(self.PATH, 'w+') as file:
            json.dump(str_data, file, indent=4)

    def set(self, value):
        self.data = value


def delta_to_string(delta):
    """Convert a timedelta into human-readable text"""
    output = ''

    days = delta.days
    seconds = delta.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days == 1:
        output += f' {days} day'
    elif days:
        output += f' {days} days'

    if hours == 1:
        output += f' {hours} hour'
    elif hours:
        output += f' {hours} hours'

    if minutes == 1:
        output += f' {minutes} minute'
    elif minutes:
        output += f' {minutes} minutes'

    if seconds == 1:
        output += f' {seconds} second'
    elif seconds:
        output += f' {seconds} seconds'

    if not output:
        output = ' 0 seconds'

    return output


def make_ordinal(n):
    """Convert an integer into its ordinal representation"""
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


class Button(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xffc300
        self.last_pressed = datetime.now()

    @commands.group(aliases=['btn'], invoke_without_command=True)
    async def button(self, ctx):
        embed = discord.Embed(title="The Button:tm:", color=self.color,
                              description=f"""It has been **????** since The Button:tm: was last pushed.
                              Feel ready? Do `{ctx.prefix}{ctx.invoked_with} push` to push it!""")
        embed.set_footer(text=f"View the leaderboard with {ctx.prefix}button lb")

        await ctx.send(embed=embed)

    @commands.max_concurrency(1, wait=True)
    @button.command(aliases=['press'])
    async def push(self, ctx):
        time_since_push = datetime.now() - self.last_pressed
        str_time = delta_to_string(time_since_push)

        with DataManager() as manager:
            if time_since_push.seconds > manager.data[ctx.author.id]:
                manager.data[ctx.author.id] = time_since_push.seconds
                manager.set(defaultdict(int, sorted(manager.data.items(), key=lambda item: item[1], reverse=True)))

            position = make_ordinal(list(manager.data.keys()).index(ctx.author.id) + 1)

        embed = discord.Embed(title="The Button:tm:", color=self.color,
                              description=f"It has been **{str_time}** since The Button:tm: was last pushed.\n"
                                          f"{ctx.author.mention} **just pushed the button**! "
                                          f"They are **{position}** in the leaderboard!")
        embed.set_footer(text=f"View the leaderboard with {ctx.prefix}button lb")
        await ctx.send(embed=embed)

        self.last_pressed = datetime.now()

    @button.command(aliases=['lb', 'top'])
    async def leaderboard(self, ctx):
        with DataManager() as manager:
            users_data = manager.data

        # convert the user ids into actual user objects
        converted_users = {ctx.guild.get_member(k): v for k, v in users_data.items()}

        leaderboard = ''
        place = ''
        index_to_emoji = {0: ':first_place:', 1: ':second_place:', 2: ':third_place:'}

        for index, user in enumerate(converted_users):
            if ctx.author.id == user.id:
                place = make_ordinal(index + 1)

            emoji = index_to_emoji.get(index, ':small_blue_diamond:')
            time = delta_to_string(timedelta(seconds=converted_users[user]))
            leaderboard += f'{emoji} **{user.mention}** • {time}\n'

        embed = discord.Embed(title="**The Button:tm: Leaderboard**", description=leaderboard, color=self.color)
        if place:
            embed.set_footer(text=f'You are {place} on the leaderboard!')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Button(bot))
