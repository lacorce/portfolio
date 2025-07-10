from aiogram.types import InlineKeyboardButton, CopyTextButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.core.config import settings
from src.database import priz_dal


def get_relevant_priz(priz_list: list):
    if not priz_list:
        return None
    priz_list.sort(key=lambda x: x.id, reverse=True)
    for priz in priz_list:
        if priz.status in [0, 1, 2, 3]:
            return priz
    return None


async def referal_keyboard(user_id):
    priz_list = await priz_dal.get_prizs(chat_id=user_id)
    priz = get_relevant_priz(priz_list)

    builder = InlineKeyboardBuilder()

    if priz and priz.status == 0:
        builder.add(InlineKeyboardButton(text='🎁 Получить награду', callback_data='get_priz_ref'))

    elif priz and priz.status == 1:
        builder.row(InlineKeyboardButton(text='⏳ Награда на проверке...', callback_data='priz_soon'))

    builder.row(InlineKeyboardButton(
        text='📨 Отправить ссылку',
        url=f'https://t.me/share/url?url={settings.bot_url}?start={user_id}')
    )
    builder.row(InlineKeyboardButton(text='📋 Скопировать ссылку', copy_text=CopyTextButton(text=f"{settings.bot_url}?start={user_id}")))
    builder.row(InlineKeyboardButton(text='📈 Таблица реферальных уровней', callback_data='referal_lvls'))
    builder.row(InlineKeyboardButton(text='‹', callback_data='back_to_menu'))

    return builder.as_markup()


async def referal_hide_lvl_keyboard(user_id):
    priz_list = await priz_dal.get_prizs(chat_id=user_id)
    priz = get_relevant_priz(priz_list)

    builder = InlineKeyboardBuilder()

    if priz and priz.status == 0:
        builder.add(InlineKeyboardButton(text='🎁 Получить награду', callback_data='get_priz_ref'))

    elif priz and priz.status == 1:
        builder.row(InlineKeyboardButton(text='⏳ Награда на проверке...', callback_data='priz_soon'))

    builder.row(InlineKeyboardButton(
        text='📨 Отправить ссылку',
        url=f'https://t.me/share/url?url={settings.bot_url}?start={user_id}')
    )
    builder.row(InlineKeyboardButton(text='📋 Скопировать ссылку', copy_text=CopyTextButton(text=f"{settings.bot_url}?start={user_id}")))
    builder.row(InlineKeyboardButton(text='📉 Скрыть таблицу реферальных уровней', callback_data='refferal'))
    builder.row(InlineKeyboardButton(text='‹', callback_data='back_to_menu'))

    return builder.as_markup()
