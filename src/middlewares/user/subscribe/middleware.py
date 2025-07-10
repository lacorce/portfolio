from typing import Callable, Dict, Any, Awaitable

from src.core import settings

from .markup import subscribe_markup

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.enums.chat_member_status import ChatMemberStatus


class SubscribeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        chat_id = event.from_user.id
        subscribe = await event.bot.get_chat_member(chat_id=settings.news_channel_id, user_id=chat_id)

        if isinstance(event, Message):
            if event.chat and event.chat.type != "private":
                if not event.message_thread_id:
                    return
                if hasattr(event, 'message_thread_id') and int(event.message_thread_id) != int(settings.topic_vpn_id):
                    return
            
        if subscribe.status == (ChatMemberStatus.LEFT or ChatMemberStatus.KICKED):
            me = await event.bot.get_me()

            bot_username = me.username
            
            await event.answer_sticker(
                sticker='CAACAgQAAxkBAAIEQWe8tQuejgnveo4tF00wBHzWpoFtAAL0FQACoalgUXoCxkTrlv3rNgQ'
            )
            await event.answer(
                text='Чтобы пользоваться нашим сервисом - <b>подпишитесь на новостной канал</b>!\n' \
                     'Для вас это <b>несколько мгновений</b>, а для нас очень приятно!',
                reply_markup=await subscribe_markup(bot_username=bot_username)
            )
        else:
            return await handler(event, data)
    
