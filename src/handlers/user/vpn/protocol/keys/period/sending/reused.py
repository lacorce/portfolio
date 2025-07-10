import asyncio
import uuid

from src.core import redis 
from src.database import payment_transactions_dal
from src.integrations import yookassa_api, cryptopay_api, check_invoice_status
from ..markup import get_course_period
from ...markup import format_number
from .markup import payment_markup, stars_payment_keyboard
from aiogram import types
from aiogram.types import LabeledPrice


def parse_sending_callback_data(callback_data: str) -> tuple:
    splitted_callback_data = callback_data.split(':')
    
    protocol = splitted_callback_data[1]
    payment_method = splitted_callback_data[2]
    key_count = int(splitted_callback_data[3])
    amount_value = float(splitted_callback_data[4])
    month_count = int(splitted_callback_data[5])
    
    return protocol, payment_method, key_count, amount_value, month_count

def get_key_text(key_count):
    if key_count == 1:
        return "1 ключ"
    elif 2 <= key_count <= 4:
        return f"{key_count} ключа"
    else:
        return f"{key_count} ключей"
    
def parse_cached_invoice(cached_invoice: str):
    invoice_params = cached_invoice.split(';')
    
    invoice_url = invoice_params[0].split('[')[1]
    protocol = invoice_params[1].split(':')[1]
    key_count = int(invoice_params[2].split(':')[1])
    month_count = int(invoice_params[3].split(':')[1])
    amount_value = float(invoice_params[4].split(':')[1])
    payment_method = invoice_params[5].split(':')[1]
    
    return invoice_url, protocol, key_count, month_count, amount_value, payment_method

async def display_sending_message(event: types.CallbackQuery, cached_invoice: str = None):
    cached_invoice = redis.get(f'invoice:{event.from_user.id}')
 
    if cached_invoice:
        await event.answer('Счет для оплаты уже создан!') 
        return
        
    if not cached_invoice:
        protocol, payment_method, key_count, amount_value, month_count = parse_sending_callback_data(callback_data=event.data)
        
        username = event.from_user.username

        if payment_method == 'yookassa':
            invoice_id, invoice_url = yookassa_api.create_invoice(
                amount_value=amount_value,
                chat_id=event.from_user.id,
                protocol=protocol,
                key_count=key_count,
                month_count=month_count,
                username=username
            )
            await payment_transactions_dal.add_payment_transaction(
                invoice_id=invoice_id,
                chat_id=event.from_user.id,
                payment_method='yookassa',
                protocol=protocol,
                config_keys=[],
                amount_value=amount_value,
                key_count=key_count,
                month_count=month_count
            )
        if payment_method == 'cryptobot':
            invoice_id, invoice_url = await cryptopay_api.create_invoice(
                amount_value=amount_value,
                chat_id=event.from_user.id,
                protocol=protocol,
                key_count=key_count,
                month_count=month_count,
                username=username
            )
            await payment_transactions_dal.add_payment_transaction(
                invoice_id=invoice_id,
                chat_id=event.from_user.id,
                payment_method='cryptobot',
                protocol=protocol,
                config_keys=[],
                amount_value=amount_value,
                key_count=key_count,
                month_count=month_count
            )
        if payment_method == 'stars':
            invoice_id, invoice_url = await cryptopay_api.create_invoice(
                amount_value=amount_value,
                chat_id=event.from_user.id,
                protocol=protocol,
                key_count=key_count,
                month_count=month_count,
                username=username
            )
            await payment_transactions_dal.add_payment_transaction(
                invoice_id=invoice_id,
                chat_id=event.from_user.id,
                payment_method='stars',
                protocol=protocol,
                config_keys=[],
                amount_value=amount_value,
                key_count=key_count,
                month_count=month_count
            )
        redis.set(
            f'invoice:{event.from_user.id}',
            f'invoice_url[{invoice_url};protocol:{protocol};key_count:{key_count};month_count:{month_count};amount_value:{amount_value};payment_method:{payment_method}',
            ex=600
        )
    else:
        invoice_url, protocol, key_count, month_count, amount_value, payment_method = parse_cached_invoice(cached_invoice)

    await event.answer(
        chat_id=event.from_user.id,
        text='Счет для оплаты был создан...'
    )

    if payment_method == 'stars':
        await event.message.delete()
        amount_stars = amount_value
        payload = f"{amount_stars}_stars_{uuid.uuid4()}"

        prices = [LabeledPrice(label="Stars", amount=amount_stars)]

        await event.bot.send_invoice(
            chat_id=event.from_user.id,
            title="Покупка ключей",
            description=f"Количество звёзд: {amount_stars}",
            payload=payload,
            provider_token="",
            currency="XTR",
            prices=prices,
            reply_markup=await stars_payment_keyboard()
        )
        return
    
    if payment_method == 'cryptobot':
        message_id = await event.message.edit_text(
            text=( 
                f'⏳ <i>Меню оплаты</i>\n\n'
                f"🛍 <b>Вы покупаете:</b> <i>{get_key_text(key_count)}</i>\n"
                f"💳 <b>Цена:</b> <i>{format_number(amount_value)} {get_course_period(payment_method)}</i>\n"
                f"📃 <b>Описание:</b>\n"
                "<i><blockquote>У вас осталось <b>5 минут</b> для завершения оплаты.</blockquote></i>"
            ),
            reply_markup=await payment_markup(url=invoice_url)
        )
        asyncio.create_task(check_invoice_status(event, invoice_id, event.from_user.id, message_id.message_id))
        redis.set(f"payment:{event.from_user.id}", message_id.message_id, ex=600)  

    if payment_method != 'cryptobot':
        message_id = await event.message.edit_text(
            text=( 
                f'⏳ <i>Меню оплаты</i>\n\n'
                f"🛍 <b>Вы покупаете:</b> <i>{get_key_text(key_count)}</i>\n"
                f"💳 <b>Цена:</b> <i>{format_number(amount_value)} {get_course_period(payment_method)}</i>\n"
                f"📃 <b>Описание:</b>\n"
                "<i><blockquote>У вас осталось <b>10 минут</b> для завершения оплаты.</blockquote></i>"
            ),
            reply_markup=await payment_markup(url=invoice_url)
        )
        redis.set(f"payment:{event.from_user.id}", message_id.message_id, ex=600)