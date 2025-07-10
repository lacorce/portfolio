from src.core.routes import user_router

from aiogram import F, types 


@user_router.callback_query(F.data == 'soon')
async def soon_callback_query_handler(callback: types.CallbackQuery):
    await callback.answer(
        text='I do it soon...'
    )
