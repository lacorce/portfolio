from src.core.routes import user_router

from .reused import display_supoprt_message

from aiogram import F, types 


@user_router.callback_query(F.data == 'support')
async def support_callback_query_handler(callback: types.CallbackQuery):
    await display_supoprt_message(event=callback)
