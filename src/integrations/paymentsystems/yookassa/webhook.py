from src.api import xui_api, RemarkEnum
from src.core import redis, settings
from src.core.routes import yookassa_router
from src.core import bot
from src.database import payment_transactions_dal, xui_configs_api
from .markup import yookassa_markup

from datetime import datetime, timedelta
from urllib.parse import quote

def get_key_form(count):
    if count == 1:
        return "1 ключ"
    elif 2 <= count <= 4:
        return f"{count} ключа"
    else:
        return f"{count} ключей"

def get_month_form(month_count):
    if month_count == 1:
        return f"{month_count} месяц"
    elif 2 <= month_count <= 4:
        return f"{month_count} месяца"
    else:
        return f"{month_count} месяцев"

@yookassa_router.post(path='/yookassa')
async def yookassa_process(body: dict):
    invoice_object = body['object']
    
    if invoice_object['status'] != 'succeeded':
        return
    
    metadata = invoice_object['metadata']
    chat_id = int(metadata['chat_id'])
    key_count = int(metadata['key_count'])
    month_count = int(metadata['month_count'])
    username = str(metadata['username'])  # This could be 'None' as a string or a valid username
    price = int(float(metadata['price']))

    message_id = redis.get(f"payment:{chat_id}")
    if message_id:
        message_id = int(message_id)
    
    config_keys = []
    emails = []
    
    for _ in range(key_count):
        config_key, client_id, email = await xui_api.add_client(
            remark=RemarkEnum.SUBSCRIPTIONS, 
            expire_time=month_count * (86400 * 30), 
            chat_id=chat_id
        )
        config_keys.append(config_key)
        emails.append(email)
        
        await xui_configs_api.add_config(
            chat_id=chat_id, client_id=client_id, 
            config_key=config_key, 
            expires_time=datetime.now().timestamp() + (month_count * 86400 * 30)
        )
    
    await payment_transactions_dal.update_payment_transaction(
        invoice_id=invoice_object['id'], 
        config_keys=config_keys, 
        status=1
    )
    
    # Modified logic for result_username
    result_username = (
        f'<a href="https://t.me/{username}"><b>Пользователь</b></a>'
        if username and username != 'None' else 'Пользователь'
    )

    if message_id:
        keys_message = (
            f'🔑 <b>Ваш ключ доступа:</b>\n'
            f'<blockquote><code>{config_keys[0]}</code></blockquote>'
            if len(config_keys) == 1 else
            f'🔑 <b>Ваши ключи доступа:</b>\n'
            f'<blockquote><code>' + '</code></blockquote>\n<blockquote><code>'.join(config_keys) + '</code></blockquote>'
        )

        now = datetime.now()
        end_time = now + timedelta(days=month_count * 30, hours=2)
        formatted_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        timezone = quote("Europe/Moscow")

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=(
                f'Оплата прошла успешно!\n\n'
                'ℹ️ <b>Информация по тарифу:</b>'
                '<blockquote>⛳️ <a href="https://www.speedtest.net/"><b>Скорость:</b></a> <i>15 mb/s</i>\n'
                f'⏳ <a href="https://embed-countdown.onlinealarmkur.com/ru/#{formatted_time}@{timezone}"><b>Срок:</b></a> <i>{get_month_form(month_count)}</i></blockquote>\n'
                f'\n'
                + keys_message
            ),
            disable_web_page_preview=True,
            reply_markup=await yookassa_markup()
        )
        
        client_message = (
            f'<a href="http://147.45.45.207:1234/0oc2pPC6o0XdiLz/panel/inbounds"><b>Client</b></a> — <code>{emails[0]}</code>\n'
        )

        if len(emails) > 1:
            client_message += '\n'.join(f'<code>{email}</code>' for email in emails[1:])

        client_message = client_message.strip()

        await bot.send_message(
            chat_id=settings.supergroup_id,
            message_thread_id=settings.topic_events_id,
            disable_web_page_preview=True,
            text='🔔 <b>New Buy</b>\n\n'
            f'{result_username} приобрел {get_key_form(key_count)}.\n\n'
            f'{client_message}\n'
            f'ID — <code>{chat_id}</code>'
        )
        transactions = await payment_transactions_dal.get_payment_transactions(status=1)
        
        total_income = sum(transaction.amount_value for transaction in transactions)
        
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        
        month_income = sum(
            transaction.amount_value 
            for transaction in transactions 
            if datetime.fromtimestamp(transaction.created_at) >= start_of_month
        )
        await bot.send_message(
            chat_id=settings.supergroup_id,
            message_thread_id=settings.topic_payments_id,
            disable_web_page_preview=True,
            text='➕ <b>New payment</b>\n\n'
                 f'<b><code>+{price} ₽</code></b>\n\n'
                 '<a href="https://yookassa.ru/my/analytics/v2/payments"><b>Заработано за месяц:</b></a> '
                 f'<code>{month_income} ₽</code> (<code>{total_income} ₽</code>)\n'
                 f'ID — <code>{chat_id}</code>'
        )
        
    redis.delete(f"payment:{chat_id}")
    redis.delete(f'invoice:{chat_id}')