from src.database import xui_configs_api, users_dal

from datetime import datetime, timedelta
from urllib.parse import quote

from src.core.routes import user_router
from src.core import bot, settings
from src.api import xui_api
from src.api.xui.api import RemarkEnum

from .markup import trial_markup

from aiogram import F, types


@user_router.callback_query(F.data == 'activate_trial')
async def trial_period_callback_handler(callback: types.CallbackQuery):
    if await users_dal.get_user(chat_id=callback.from_user.id, trial_period=True):
        await callback.answer('🤨')
        return

    try:
        config_key, client_id, email = await xui_api.add_client(
            remark=RemarkEnum.TEMPORARY,
            chat_id=callback.from_user.id,
            expire_time=604800
        )
    except Exception as e:
        await callback.answer("❌")
        return
    
    expire_time = 604800 

    result_username = (
        f'<a href="https://t.me/{callback.from_user.username}"><b>Пользователь</b></a>'
        if callback.from_user.username else 'Пользователь'
    )

    await xui_configs_api.add_config(
        chat_id=callback.from_user.id,
        client_id=email,
        config_key=config_key,
        expires_time=expire_time + datetime.now().timestamp()
    )
    
    await users_dal.update_user(chat_id=callback.from_user.id, trial_period=1)

    await bot.send_message(chat_id=settings.supergroup_id, 
                           message_thread_id=settings.topic_events_id, 
                           text='🔔 <b>Notification</b>\n\n'
                           f'{result_username} активировал тестовый ключ.\n\n'
                           f'<a href="http://147.45.45.207:1234/0oc2pPC6o0XdiLz/panel/inbounds"><b>Client</b></a> — <code>{email}</code>\n'
                           f'ID — <code>{callback.from_user.id}</code>',
                            disable_web_page_preview=True
                        )

    now = datetime.now()
    end_time = now + timedelta(days=7, hours=2)
    formatted_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    timezone = quote("Europe/Moscow")

    await callback.message.edit_text(
        text=
            'Вы активировали тестовый период!\n\n'
            'ℹ️ <b>Информация по тарифу:</b>'
            '<blockquote>⛳️ <a href="https://www.speedtest.net/"><b>Скорость:</b></a> <i>2-4 mb/s</i>\n'
            '📦 <b>Трафик:</b> <i>30 gb</i>\n'
            f'⏳ <a href="https://embed-countdown.onlinealarmkur.com/ru/#{formatted_time}@{timezone}"><b>Срок:</b></a> <i>7 дней</i></blockquote>\n\n'
            '🔑 <b>Ваш ключ доступа:</b>\n'
            f'<code><blockquote>{config_key}</blockquote></code>\n\n',
        disable_web_page_preview=True,
        reply_markup= await trial_markup()
    )
