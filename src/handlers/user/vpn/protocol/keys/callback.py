from src.core.routes import user_router

from .reused import display_keys_message

from aiogram import types, F


@user_router.callback_query(F.data.startswith('payment_method:'))
async def buy_vless_callback_handler(callback: types.CallbackQuery):
    await display_keys_message(event=callback)