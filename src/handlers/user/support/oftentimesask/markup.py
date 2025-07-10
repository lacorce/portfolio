from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def oftentimes_ask_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.add(
        types.InlineKeyboardButton(
            text='Какими способами я могу оплатить покупку?',
            callback_data='oftentimes_ask:1'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Как настроить VPN?',
            callback_data='oftentimes_ask:2'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Какие протоколы шифрования используются в вашем VPN?',
            callback_data='oftentimes_ask:3'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Где находятся ваши сервера?',
            callback_data='oftentimes_ask:4'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Есть ли ограничения по скорости и объему трафика при использовании VPN?',
            callback_data='oftentimes_ask:5'
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Могу ли я передать свой ключ другу для пользования ?',
            callback_data='oftentimes_ask:6'
        )
    )

    builder.row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data='support'
        ),
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu'
        )
    )
    return builder.as_markup()

async def how_to_setup_vpn():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='«',
            callback_data='back_to_menu'
        )
    )
    return builder.as_markup()   
