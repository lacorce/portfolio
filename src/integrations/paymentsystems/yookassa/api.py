import uuid

from src.core import settings

from yookassa import Configuration, Payment


Configuration.account_id = f'{settings.yookassa_shop_id}'
Configuration.secret_key = f'{settings.yookassa_secret_key}'


class YooKassaAPI:
    def create_invoice(self, amount_value: int, chat_id: int, protocol: str, key_count: int, month_count: int, username: str) -> str:
        payment = Payment.create({
            'amount': {
                'value': f'{amount_value}',
                'currency': 'RUB'
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': 'https://t.me/radjavpnbot'
            },
            'capture': True,
            'description': 'Покупка ключа / 💛 RadjaVPN',
            'metadata': {
                'chat_id': f'{chat_id}',
                'protocol': f'{protocol}',
                'key_count': f'{key_count}',
                'month_count': f'{month_count}',
                'username': f'{username}',
                'price': f'{amount_value}'
            }
        }, uuid.uuid4())
        
        return payment.id, payment.confirmation.confirmation_url
