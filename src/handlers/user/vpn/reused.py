from src.core import redis
from .markup import buy_vpn_markup
from .protocol.keys.period.sending.reused import display_sending_message

from aiogram import types 


def get_buy_vpn_text() -> str:
    
    return('🔑 <i>Меню покупки VPN</i>\n\n'
           '<blockquote><i><a href="https://t.me/radjavpnbot?start=vless"><b>🪁 VLESS (V2Ray Less)</b></a> — это протокол для обхода блокировок и обеспечения приватности в интернете. Он является улучшенной версией протокола VMess (используемого в V2Ray) и был разработан с целью повышения производительности и безопасности.</i></blockquote>')
    
    
async def display_buy_vpn_message(event: types.CallbackQuery):
    chat_id = event.from_user.id
    message_id = event.message.message_id
    
    buy_vpn_text = get_buy_vpn_text()
    
    await event.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=buy_vpn_text,
        reply_markup=await buy_vpn_markup(),
        disable_web_page_preview=True
    )
