from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def select_currencies_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text="USD", callback_data="currency_USD"),
        types.InlineKeyboardButton(text="EUR", callback_data="currency_EUR"),
        types.InlineKeyboardButton(text="RUB", callback_data="currency_RUB"))

    return builder.as_markup()  

async def select_transaction_type_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        types.InlineKeyboardButton(text="Доход", callback_data="transaction_type_income"),
        types.InlineKeyboardButton(text="Трата", callback_data="transaction_type_expense"))

    return builder.as_markup()  