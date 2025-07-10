from src.core import redis
from src.core.routes import user_router

from .reused import display_menu_messages

from aiogram import F, types 
from aiogram.fsm.context import FSMContext

@user_router.callback_query(F.data.in_(['back_to_menu', 'back_to_menu_state_clear', 'back_to_menu_state_star_clear']))
async def back_to_menu_callback_query_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_menu_state_clear':
        redis.delete(f'invoice:{callback.from_user.id}')
    if callback.data == 'back_to_menu_state_star_clear':    
        await callback.message.delete()      
        await display_menu_messages(event=callback, edit=False, sticker_status=False)
        redis.delete(f'invoice:{callback.from_user.id}')
        return
    
    await display_menu_messages(event=callback, edit=True)
