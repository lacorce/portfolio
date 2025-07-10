from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def buy_vpn_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text='🪁 VLESS',
            callback_data='buy:vless'
        )
    ).row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data='back_to_menu'
        )
    )
    return builder.as_markup()
