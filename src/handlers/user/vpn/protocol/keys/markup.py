from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core import redis
from src.scheduler.jobs import cache_exchange_rates

async def get_course(payment_method_number: int) -> str:
    courses = {
        1: {
            'name': 'cryptobot',
            'symbol': '$',
            'rate': None
        },
        2: {
            'name': 'yookassa',
            'symbol': '₽',
            'rate': 1
        },
        3: {
            'name': 'stars',
            'symbol': '🌟',
            'rate': 1
        }
    }
    
    if payment_method_number == 1:
        rate = redis.get('rub_usd_rate')
        
        if rate is None:
            await cache_exchange_rates()
            rate = redis.get('rub_usd_rate')

        if rate is None:
            raise ValueError("Курс 'rub_usd_rate' не удалось получить даже после обновления.")

        courses[1]['rate'] = float(rate.decode('utf-8'))

    return courses[payment_method_number]


def format_number(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    else:
        return round(value, 2)


async def keys_markup(protocol: str, payment_method_number: int) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    course = await get_course(payment_method_number=payment_method_number)    

    base_price = 50 if payment_method_number == 3 else 77

    builder.add(
        types.InlineKeyboardButton(
            text=f'🔑 1 ключ — всего {format_number(base_price * course["rate"])} {course["symbol"]}',
            callback_data=f'finish:{protocol}:{course["name"]}:1:{format_number(base_price * course["rate"])}'
        )
    ).row(
        types.InlineKeyboardButton(
            text=f'🔑 2 ключа — {format_number(150 * course["rate"] if payment_method_number != 3 else 80)} {course["symbol"]}',
            callback_data=f'finish:{protocol}:{course["name"]}:2:{format_number(150 * course["rate"] if payment_method_number != 3 else 80)}'
        )
    ).row(
        types.InlineKeyboardButton(
            text=f'🔑 3 ключа — {format_number(250 * course["rate"] if payment_method_number != 3 else 120)} {course["symbol"]}',
            callback_data=f'finish:{protocol}:{course["name"]}:3:{format_number(250 * course["rate"] if payment_method_number != 3 else 120)}'
        )
    ).row(
        types.InlineKeyboardButton(
            text=f'🔑 4 ключа — {format_number(300 * course["rate"] if payment_method_number != 3 else 160)} {course["symbol"]}',
            callback_data=f'finish:{protocol}:{course["name"]}:4:{format_number(300 * course["rate"] if payment_method_number != 3 else 160)}'
        )
    ).row(
        types.InlineKeyboardButton(
            text=f'🔑 5 ключей — {format_number(400 * course["rate"] if payment_method_number != 3 else 200)} {course["symbol"]}',
            callback_data=f'finish:{protocol}:{course["name"]}:5:{format_number(400 * course["rate"] if payment_method_number != 3 else 200)}'
        )
    ).row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data=f'buy:{protocol}'
        ),
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu'
        )
    )

    return builder.as_markup()
