from aiogram import F
from src.api import xui_api, RemarkEnum
from src.core import settings
from src.database import xui_configs_api
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from src.database import priz_dal
from src.core.routes import user_router
from .markup import delete_message
from datetime import datetime

@user_router.callback_query(F.data.startswith("requestpriz_"))
async def handle_priz_request(callback_query: CallbackQuery):
    data = callback_query.data.split('_')

    if len(data) != 5:
        return

    chat_id = int(data[1])
    lvl = int(data[2])
    priz_id = int(data[3])
    action = data[4]

    expire_seconds = 86400 * 30
    duration_text = "1 месяц"

    if lvl == 1:
        expire_seconds = 86400 * 7
        duration_text = "7 дней"
    elif lvl == 2:
        expire_seconds = 86400 * 14
        duration_text = "14 дней"
    elif lvl == 3:
        expire_seconds = 86400 * 30
        duration_text = "1 месяц"
    elif lvl == 4:
        expire_seconds = 86400 * 30 * 3
        duration_text = "3 месяца"
    elif lvl == 5:
        expire_seconds = 86400 * 30 * 6
        duration_text = "6 месяцев"
    
    if action == 'yes':
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅", callback_data="no_data")]
        ])
        config_keys = []
        emails = []

        for _ in range(1):
            config_key, client_id, email = await xui_api.add_client(
                remark=RemarkEnum.SUBSCRIPTIONS,
                expire_time=expire_seconds,
                chat_id=chat_id
            )

            config_keys.append(config_key)
            emails.append(email)

            await xui_configs_api.add_config(
                chat_id=chat_id,
                client_id=client_id,
                config_key=config_key,
                expires_time=datetime.now().timestamp() + expire_seconds
            )

        keys_message = (
            f'🔑 <b>Ваш ключ доступа:</b>\n'
            f'<blockquote><code>{config_keys[0]}</code></blockquote>'
        )

        await callback_query.bot.send_message(
            chat_id=chat_id,
            text=f'Вы получили подарок за приглашенных рефералов:\n\n{keys_message}\nСрок действия: {duration_text}',
            reply_markup=await delete_message()
        )

        client_message = (
            f'<b>Client</b> — <code>{emails[0]}</code>\n'
        )

        if len(emails) > 1:
            client_message += '\n'.join(f'<code>{email}</code>' for email in emails[1:])

        client_message = client_message.strip()

        await callback_query.bot.send_message(
            chat_id=settings.supergroup_id,
            message_thread_id=settings.topic_events_id,
            disable_web_page_preview=True,
            text='🔔 <b>Refferal Key</b>\n\n'
            f'<b>Пользователь</b> получил ключ за реферала.\n\n'
            f'{client_message}\n'
            f'ID — <code>{chat_id}</code>'
        )

        await priz_dal.update_priz_by_id(priz_id, status=2)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚫", callback_data="no_data")]
        ])
        await priz_dal.update_priz_by_id(priz_id, status=3)

    await callback_query.message.edit_reply_markup(reply_markup=markup)

@user_router.callback_query(F.data == 'delete_message')
async def delete_message_keyboard_handler(call: CallbackQuery):
    await call.message.delete()