from src.core.routes import user_router

from .reused import display_oftentimes_ask_message, display_answer_to_oftentimes_ask

from aiogram import F, types


@user_router.callback_query(F.data == 'oftentimes_ask')
async def oftentimes_ask_callback_query_handler(callback: types.CallbackQuery):
    await display_oftentimes_ask_message(event=callback)


@user_router.callback_query(F.data.startswith('oftentimes_ask:'))
async def answer_to_oftentimes_ask_callback_query_handler(callback: types.CallbackQuery):
    await display_answer_to_oftentimes_ask(event=callback)
