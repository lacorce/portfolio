from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def payment_method(protocol: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
        types.InlineKeyboardButton(
            text='👾 CryptoBot',
            callback_data=f'payment_method:{protocol}:cryptobot'
        )
    ).row(
        types.InlineKeyboardButton(
            text='💳 Картой (СБП)',
            callback_data=f'payment_method:{protocol}:yookassa'
        )
    ).row(
        types.InlineKeyboardButton(
            text='🌟 Stars',
            callback_data=f'payment_method:{protocol}:stars'
        )
    ).row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data='vpn'
        ),
        (
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu'
        )
    )
    )

    return builder.as_markup()
