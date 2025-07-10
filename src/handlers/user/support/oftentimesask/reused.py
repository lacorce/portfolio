from .markup import oftentimes_ask_markup, how_to_setup_vpn

from aiogram import types 


async def display_oftentimes_ask_message(event: types.CallbackQuery):
    await event.message.edit_text(
        text='📚 <i>Меню часто задаваемых вопросов</i>',
        reply_markup=await oftentimes_ask_markup()
    )
  
def get_ask_number(callback_data: str) -> int:
    splitted_callback_data = callback_data.split(':')
    
    ask_number = int(splitted_callback_data[1])
    
    return ask_number
  
  
def get_answer(ask_number: int) -> str:
    answers = {
        1: '— CryptoBot, YooMoney, Telegram Stars.\nВы можете выбрать удобный для вас!',
        2: '',
        3: '— На данный момент мы используем VLESS протоколы.',
        4: '— На данный момент у нас сервера в Нидерландах.',
        5: '— Да, в пробном периоде включены ограничения по скорости и обьему. Полноценный работает без ограничений.',
        6: '— Да, но пользоваться сможет только один активный пользователь.'
    }
    
    return answers[ask_number]
    
    
async def display_answer_to_oftentimes_ask(event: types.CallbackQuery): 
    ask_number = get_ask_number(callback_data=event.data)
    answer = get_answer(ask_number=ask_number)

    if ask_number == 2:
        await event.message.edit_text(
            text=(
                '📝 <i>Как настроить VPN?</i>\n\n'
                '<code>1.</code> Установите <b><a href="https://github.com/2dust/v2rayN/releases/tag/7.9.3">v2rayN</a></b>, '
                '<b><a href="https://en.nekoray.org/">NekoRay</a></b> (для ПК) или <b>V2Box</b> (для телефонов).\n\n'
                '<code>2.</code> Скопируйте ваш <b>ключ</b> подключения.\n\n'
                '<code>3.</code> Откройте приложение и нажмите:\n'
                '   — <b>Servers</b>\n'
                '   — <b>Import Share Links from clipboard</b>\n\n'
                '<code>4.</code> Нажмите <b>Clear system proxy</b>\n'
                '   (если у вас отображается <i>Set system proxy</i> — ничего не меняем)\n\n'
                '<code>5.</code> Готово! Пользуйтесь нашим VPN ❤️'
            ),
            reply_markup=await how_to_setup_vpn(),
            disable_web_page_preview=True
        )
    else:
        await event.answer(text=answer, show_alert=True)