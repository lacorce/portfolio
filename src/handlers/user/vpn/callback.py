from src.core.routes import user_router

from .reused import display_buy_vpn_message

from aiogram import types, F


@user_router.callback_query(F.data == 'vpn')
async def buy_vpn_callback_handler(callback : types.CallbackQuery):
    await display_buy_vpn_message(event=callback)
    