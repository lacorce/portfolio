from aiogram import types

from .markup import support_markup


def get_support_text():
    return ('💬 <i>Меню помощи и поддержки</i>\n\n'
            'Прежде чем задать свой вопрос, пожалуйста, <b>ознакомьтесь с информацией, перейдя по кнопке <i>„📚 Часто задаваемые вопросы“</i></b>.\n\n'
            'Если вы не нашли ответ на свой вопрос, пожалуйста, <b>при обращении следуйте следующим рекомендациям:</b>\n\n'
            '<blockquote expandable><i>1. Четко сформулируйте свой вопрос или проблему. Укажите, что именно вызывает трудности.\n\n'
            '2. Не отправляйте вопросы, не относящиеся к теме. Это поможет нам быстрее решить вашу проблему.\n\n'
            '3. Убедитесь, что в вашем сообщении нет лишней информации или излишних уточнений — так мы сможем быстрее разобраться в ситуации.\n\n'
            '4. Если ваша проблема техническая, уточните, какое устройство или приложение вы используете, а также укажите, какие шаги вы уже предприняли.\n\n'
            '5. Если возможно, прикрепите скриншоты или лог ошибок — это поможет нам быстрее понять и устранить проблему.</i></blockquote>'
            )
    
async def display_supoprt_message(event: types.CallbackQuery):
    chat_id = event.from_user.id
    message_id = event.message.message_id
    
    support_text = get_support_text()
    
    await event.bot.edit_message_text(
        chat_id=chat_id, 
        message_id=message_id,
        text=support_text,
        reply_markup=await support_markup()
    )