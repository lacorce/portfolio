from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def history_markup(has_keys: bool, has_coupons: bool) -> types.InlineKeyboardMarkup | None:
    if has_keys and has_coupons:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text='🪪 Купоны', callback_data='cupon_history'))
        builder.row(types.InlineKeyboardButton(text='🔑 Ключи', callback_data='key_history'))
        builder.row(types.InlineKeyboardButton(text='‹', callback_data='back_to_menu'))
        return builder.as_markup()
    return None

async def back_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='‹', callback_data='back_to_menu'))
    return builder.as_markup()