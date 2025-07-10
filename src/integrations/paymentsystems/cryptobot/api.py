import json
import aiohttp

from src.core import settings


class CryptoPayAPI:
    def __init__(self):
        self.base_url = settings.cryptobot_url
        self.secret_key = settings.cryptobot_secret_key
        
        self.headers = {
            'Crypto-Pay-API-Token': self.secret_key
        }
        
    def _make_url(self, endpoint: str) -> str:
        return f'{self.base_url}/{endpoint}'
        
    async def _make_request(self, method: str, url: str, headers: dict = None, data: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, headers=self.headers, data=data) as response:
                return await response.json()

    async def get_exchange_rates(self) -> dict:
        method = 'GET'
        endpoint = 'getExchangeRates'
        
        response_json = await self._make_request(method=method, url=f'{self._make_url(endpoint)}')
        
        return response_json['result']
    
    async def create_invoice(self, chat_id: int, protocol: str, key_count: int, month_count: int, amount_value: float, username: str):
        method = 'POST'
        endpoint = 'createInvoice'
        payload_dict = {
            'protocol': protocol,
            'chat_id': chat_id,
            'key_count': key_count,
            'month_count': month_count,
            'username': username,
            'price': amount_value
        }
        payload_str = json.dumps(payload_dict)

        data = {
            'asset': 'USDT',
            'amount': amount_value,
            'payload': payload_str
        }
        
        response_json = await self._make_request(method=method, url=f'{self.base_url}/{endpoint}', data=data)
        
        invoice_obj = response_json['result']
        
        invoice_id = str(invoice_obj['invoice_id'])
        invoice_url = invoice_obj['pay_url']
        
        return invoice_id, invoice_url
    
    async def get_invoice_status(self, invoice_id: str) -> str:
        method = 'GET'
        endpoint = f'getInvoices'
        params = {
            'invoice_ids': invoice_id,
        }
        response_json = await self._make_request(method=method, url=f'{self._make_url(endpoint)}', data=params)

        return response_json