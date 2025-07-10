from aiogram import types, F

from src.core.routes import user_router

from ..markup import referal_hide_lvl_keyboard


@user_router.callback_query(F.data == 'referal_lvls')
async def referal_lvls_keyboard_handler(callback : types.CallbackQuery):
    await callback.message.edit_text(
        text=f'📈 <i>Меню таблицы реферальных уровней</i>\n'
        '<a href="https://i.ibb.co/4wFm9ntm/image-2025-03-23-04-38-37.png">ᅠ</a>',
    reply_markup=await referal_hide_lvl_keyboard(user_id=callback.from_user.id)
    )

