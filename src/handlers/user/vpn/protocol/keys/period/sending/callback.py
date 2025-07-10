from src.core.routes import user_router
from .filter import IsPaymentMethodStarsFilter
from .reused import display_sending_message
from aiogram import F, types


@user_router.callback_query(F.data.startswith('sending:'))
async def finish_callback_handler(callback: types.CallbackQuery):
     await display_sending_message(event=callback)