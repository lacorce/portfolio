from aiogram import types
from .markup import period_markup


def get_keys_text() -> str:
    return(f'🔑 <i>Меню выбора периода действия ключа</i>\n\n'
           '🔐 <b>Важно:</b> Срок действия ключа выбирается один раз при покупке и не подлежит изменению.\n\n'
           '<blockquote><i>Мы не несем ответственности за ошибки при выборе срока, передачу ключа третьим лицам или его несанкционированное использование. </i></blockquote>\n')


async def display_finish_message(event: types.CallbackQuery):  
    splitted_callback_data = event.data.split(':')
    protocol = splitted_callback_data[1]
    payment_method = splitted_callback_data[2]
    amount_keys = splitted_callback_data[3]
    start_amount = splitted_callback_data[4]

    keys_text = get_keys_text() 

    await event.message.edit_text(
        text=keys_text,reply_markup=await period_markup(protocol=protocol, payment_method=payment_method,amount_keys=amount_keys, start_amount=start_amount)
     )