import aiohttp
from src.core import open_config

async def create_invoice(amount: float, currency="USDT", webhook_url=None):
    url = f"https://pay.crypt.bot/api/invoices/create"
    headers = {
        "Authorization": f"Bearer {open_config('api_key')}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": amount,
        "currency": currency,
        "description": "Пополнение баланса",
    }
    if webhook_url:
        payload["webhook_url"] = webhook_url

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            data = await resp.json()
            if resp.status == 200:
                return data
            else:
                print("Ошибка создания инвойса:", data)
                return None

async def check_invoice_status(invoice_id: str):
    url = f"https://pay.crypt.bot/api/invoices/{invoice_id}"
    headers = {
        "Authorization": f"Bearer {open_config('api_key')}",
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            if resp.status == 200:
                return data
            else:
                print("Ошибка проверки инвойса:", data)
                return None
