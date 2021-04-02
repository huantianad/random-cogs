import aiohttp


async def get_level_data(url):
    """Tries to find a level with the same url on the site, if it fails, return None"""
    api_url = 'https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec'

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            r = await response.json()

    try:
        return next(x for x in r if x['download_url'] == url)
    except StopIteration:
        return None
