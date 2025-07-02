import aiohttp

async def convert_rub_to_usdt(rub_amount: float) -> float:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("error conv api")
            data = await response.json()
            price_rub = data["tether"]["rub"]
            usdt = round(rub_amount / price_rub, 2)
            return usdt
