from .markup import keys_markup
from aiogram import types

def get_keys_text(emoji) -> str:
    return(f'{emoji} <i>Меню выбора кол-ва ключей</i>\n\n'
           '🔐 <b>Важно:</b> Ключ выдается в одни руки.\n\n'
           '<blockquote><i>Мы не несем ответственности за любые проблемы, возникшие в случае передачи ключа третьим лицам или его несанкционированного использования.</i></blockquote>\n')

def parse_keys_callback_data(callback_data: str):
    splitted_callback_data = callback_data.split(':')

    payment_methods_numbers = {
        'cryptobot': 1,
        'yookassa': 2,
        'stars': 3
    }

    match splitted_callback_data[2]:
        case 'cryptobot':
            emoji = '👾'
        case 'yookassa':
            emoji = '💳'
        case 'stars':
            emoji = '🌟'
    
    protocol = splitted_callback_data[1]
    payment_method = splitted_callback_data[2]
    
    return protocol, payment_methods_numbers[payment_method], emoji


async def display_keys_message(event: types.CallbackQuery):
    protocol, payment_method_number, emoji = parse_keys_callback_data(callback_data=event.data)
    
    keys_text = get_keys_text(emoji) 
    
    await event.message.edit_text(
        text=keys_text,
        reply_markup=await keys_markup(protocol=protocol, payment_method_number=payment_method_number)
    )