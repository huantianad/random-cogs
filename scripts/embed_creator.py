from datetime import datetime

from discord import Embed, Color


def create_embed(data):
    """Takes the level information and returns the embed that has blend stuff."""
    date = datetime.now().strftime("%a, %b %d, %Y")

    modes = []
    if data['single_player']:
        modes.append("1P")
    if data['two_player']:
        modes.append("2P")

    embed = Embed(title=f"Daily Blend: {date}", color=Color.purple())
    embed.add_field(name="Level", value=f"{data['artist']} - {data['song']}")
    embed.add_field(name="Creator", value=data['author'])
    embed.add_field(name="Description", value=data['description'], inline=False)
    embed.add_field(name="Tags", value=", ".join([f'**[{x}]**' for x in data['tags']]), inline=False)
    embed.add_field(name="Modes", value=" ".join(modes))
    embed.add_field(name="Difficulty", value=data['difficulty'])
    embed.add_field(name="Download", value=f"[Link]({data['download_url']})", inline=True)
    embed.set_image(url=data['preview_img'])

    return embed


info_embed = Embed(title="About the Daily Blend Café",
                   description="The Daily Blend Café is like a book club for custom levels! Play the daily level and "
                               "post your score (press shift-o after loading the level to enable detailed scoring), "
                               "and leave a comment with what you liked about the level!")

confirm_embed = Embed(title="Confirm Blend", description="Are you sure you want to send this blend?")
success_embed = Embed(title="Success", description="The level was successfully blended.", color=Color.green())
cancel_embed = Embed(ttile="Canceled", description="The blend was canceled.", color=Color.red())
