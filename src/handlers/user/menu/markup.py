from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def menu_markup(result) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if not result: 
        builder.add(types.InlineKeyboardButton(text='✨ Активировать тестовый период', callback_data='activate_trial'))

    builder.row(types.InlineKeyboardButton(text='🫂 Реферальная система', callback_data='refferal'),
                types.InlineKeyboardButton(text='🔑 Купить VPN', callback_data='vpn'))

    
    if result:
        builder.row(types.InlineKeyboardButton(text='⚙️ Мой VPN', callback_data='my_vpn'))

    #if result:
    #    builder.row(types.InlineKeyboardButton(text='🗂 История', callback_data='history'))

    builder.row(types.InlineKeyboardButton(text='🧩 Наши сервисы', url='https://t.me/radjanews/6'))

    builder.row(types.InlineKeyboardButton(text='💬 Помощь и поддержка', callback_data='support'))
    
    return builder.as_markup()

async def controls_markup() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text='📊 Статистика', callback_data='iwniwnggwg'))

    builder.row(types.InlineKeyboardButton(text='📢 Рассылка', callback_data='wgweg'),
                types.InlineKeyboardButton(text='👥 Пользователи', callback_data='regwrg'))

    builder.row(types.InlineKeyboardButton(text='⌨️ Добавить хост', callback_data='wgw33'))
    
    return builder.as_markup()