from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def main_user_menu_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text='📊 Мои финансы', callback_data='finances'))

    builder.row(
        types.InlineKeyboardButton(text='➕ Добавить транзакцию', callback_data='add_transaction'),
        types.InlineKeyboardButton(text='📈 Отчеты и графики', callback_data='reports'))

    #builder.row(
    #    types.InlineKeyboardButton(text='💱 Валюты', callback_data='currencies'),
    #    types.InlineKeyboardButton(text='⚙️ Настройки ', callback_data='settings'))

    return builder.as_markup()
