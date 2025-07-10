import aiohttp

from src.core import redis
from src.integrations import cryptopay_api


async def cache_exchange_rates():
    for exchange_rate in await cryptopay_api.get_exchange_rates():
        if exchange_rate['source'] == 'RUB' and exchange_rate['target'] == 'USD':
            redis.set(name='rub_usd_rate', value=round(float(exchange_rate['rate']), 3))
