from aiogram import F, types

from src.core.routes import user_router
from src.core.config import settings
from src.database import users_dal

from .markup import referal_keyboard


@user_router.callback_query(F.data == 'refferal')
async def ref_system_keyboard_handler(callback: types.CallbackQuery):

    referral_count = await users_dal.get_users(referral_owner_chat_id=callback.from_user.id)

    referral_count = len(referral_count)

    referral_lvls = settings.referral_lvls
    referral_level = 0

    for lvl, threshold in enumerate(referral_lvls, start=1):
        if referral_count >= threshold:
            referral_level = lvl

    await callback.message.edit_text(
        text=(
            '🫂 <i>Меню реферальной системы</i>\n\n'
            f'🎯 Ваш реферальный уровень: <i><code>{referral_level}</code> lvl</i>\n'
            f'👨‍👩‍👧‍👦 Всего приглашенных: <i><code>{referral_count}</code> человек</i>\n\n'
            '<a href="https://telegra.ph/Referalnaya-sistema-04-10"><b>FAQ реферальная система</b></a>'
        ),
        disable_web_page_preview=True,
        reply_markup=await referal_keyboard(user_id=callback.from_user.id)
    )
