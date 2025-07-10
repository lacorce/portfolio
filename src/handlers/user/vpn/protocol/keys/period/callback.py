from src.core.routes import user_router
from .reused import display_finish_message

from aiogram import types, F


@user_router.callback_query(F.data.startswith('finish:'))
async def finish_callback_handler(callback: types.CallbackQuery):
     await display_finish_message(event=callback)
