from src.core.routes import user_router

from .reused import display_payment_method_message

from aiogram import F, types


@user_router.callback_query(F.data.startswith('buy:'))
async def select_payment_method(callback : types.CallbackQuery):
    await display_payment_method_message(event=callback)
    