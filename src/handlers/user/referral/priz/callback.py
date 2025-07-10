from aiogram import types, F

from src.core.routes import user_router
from src.core import settings
from src.database import priz_dal, users_dal
from .markup import back_refferal, request_to_admin_keyboard


@user_router.callback_query(F.data == 'get_priz_ref')
async def get_priz_refferal_keyboard_handler(call: types.CallbackQuery):
    all_prizs = await priz_dal.get_prizs(chat_id=call.from_user.id)
    priz = next((p for p in all_prizs if p.status == 0), None)

    if not priz:
        print('!!!123!!!')
        await call.answer('🤨')
        return

    await call.answer('Заявка на получение награды отправлена...')
    await call.message.edit_text(
        text='🎁 <i>Меню полученя награды</i>\n\n'
             '<b>Пожалуйста, подождите немного, и вы получите награду как только проверка будет завершена успешно.</b>\n'
             'Спасибо, что вы с нами!',
        reply_markup=await back_refferal()
    )

    await priz_dal.update_priz_by_id(priz.id, status=1)

    referrals = await users_dal.get_users(referral_owner_chat_id=call.from_user.id)
    referral_count = len(referrals)
    referrals_str = ', '.join([str(ref.chat_id) for ref in referrals])

    await call.bot.send_message(
        chat_id=settings.supergroup_id,
        message_thread_id=settings.topic_request_id,
        text=f'🗳 <b>New request</b>\n\n<b>From: <code>{call.from_user.id}</code></b>\n\n<b>Ref sum:</b> <code>{referral_count}</code>\n\n'
             f'<b>All referrals:</b> <code>{referrals_str}</code>',
        reply_markup=await request_to_admin_keyboard(chat_id=call.from_user.id, lvl=priz.lvl, id = priz.id)
    )


@user_router.callback_query(F.data == 'priz_soon')
async def priz_soon_keyboard_handler(call: types.CallbackQuery):
    await call.answer('Ожидайте, скоро вашу заявку рассмотрят!')