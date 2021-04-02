from discord.ext import commands, tasks

from scripts.site import get_level_data
from scripts import embed_creator


class Blender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main_loop.start()

        self.daily_blend_channel_id = 772631203337338920

    async def user_confirm(self, ctx):
        """Sends a message that the user has to react to to either confirm or deny an action
        In this case, the check to confirm outputs True, deny outputs False"""
        check_emojis = ["✔️", "✖️"]

        # Sends the message that the user will react to, react with possible options
        message = await ctx.send(embed=embed_creator.confirm_embed)
        for emoji in check_emojis:
            await message.add_reaction(emoji)

        def check(r, u):
            return r.emoji in check_emojis and u == ctx.author and r.message == message

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        return reaction.emoji == check_emojis[0]  # True when user reacts with check, false when x

    @commands.command()
    async def blend(self, ctx, url):
        """Blends a level, given a level's url"""

        async with ctx.typing():  # This might take a bit, so use typing() to indicate that
            level_data = await get_level_data(url)

        if level_data is None:
            await ctx.send(f"Oh no! The level `{url}` was not found.")
            return

        # Makes the actual embed
        blend_embed = embed_creator.create_embed(level_data)

        # Send a preview to the user, have them make sure it's correct and confirm it
        await ctx.send(embed=blend_embed)
        confirmed = await self.user_confirm(ctx)

        if confirmed:
            # If they react with the checkmark to confirm
            daily_blend_channel = ctx.guild.get_channel(self.daily_blend_channel_id)  # Get the channel object
            channel_webhook = (await daily_blend_channel.webhooks())[0]  # Then take the first webhook to send embed

            await channel_webhook.send(embeds=[blend_embed, embed_creator.info_embed])

            # Unpin old blend, pin new blend
            pins = await daily_blend_channel.pins()
            sorted_pins = sorted(pins, key=lambda x: x.created_at)  # Sort by date created to unpin the newest
            await sorted_pins[0].unpin()
            await daily_blend_channel.last_message.pin()  # Pin the latest message, which should be the blend

            await ctx.send(embed=embed_creator.success_embed)
        else:
            # The blend got canceled by user.
            await ctx.send(embed=embed_creator.cancel_embed)

    @tasks.loop(minutes=1.0)
    async def main_loop(self):
        pass

    @main_loop.before_loop
    async def before_main(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.main_loop.cancel()


def setup(bot):
    bot.add_cog(Blender(bot))
