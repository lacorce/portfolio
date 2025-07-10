from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .utils import extract_uuid 

async def my_vpn_markup(configs: list = None, expired_configs: list = None) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if configs:
        for config in configs:
            uuid = extract_uuid(config.config_key)
            builder.row(
                types.InlineKeyboardButton(
                    text=f'{uuid[:10]}...',
                    callback_data=f'vpn_detail:{uuid}'
                )
            )

    if expired_configs:
        for config in expired_configs:
            uuid = extract_uuid(config.config_key)
            builder.row(
                types.InlineKeyboardButton(
                    text=f'❌ {uuid[:10]}...',
                    callback_data='expired_soon'
                )
            )

    builder.row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data='back_to_menu'
        )
    )

    return builder.as_markup()

async def back_to_menu() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text='‹',
            callback_data='back_to_menu'
        )
    )

    return builder.as_markup()