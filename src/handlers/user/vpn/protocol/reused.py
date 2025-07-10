from .markup import payment_method

from aiogram import types 


def get_payment_method_text() -> str:
    return('🪁 <i>Меню выбора способа оплаты</i>')


def get_protocol(callback_data: str) -> str: 
    splitted_callback_data = callback_data.split(':')
    
    protocol = splitted_callback_data[1]

    return protocol


async def display_payment_method_message(event: types.CallbackQuery | types.Message, protocol: str = None, send: bool = False):
    protocol = get_protocol(callback_data=event.data) if not protocol else protocol
    payment_method_text = get_payment_method_text()
    
    if send:
        chat_id = event.from_user.id 
        
        await event.bot.send_message(
            chat_id=chat_id,
            text=payment_method_text, 
            reply_markup=await payment_method(protocol=protocol)
        )
        
        return
    
    await event.message.edit_text(
        text=payment_method_text, 
        reply_markup=await payment_method(protocol=protocol)
    )
