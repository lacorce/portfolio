from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.database import users_dal

class ExistsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = await users_dal.get_user(chat_id=event.from_user.id)
        if not user:
            await users_dal.add_user(chat_id=event.from_user.id, username=f'@{event.from_user.username}')
            user = await users_dal.get_user(chat_id=event.from_user.id)

        if f'@{event.from_user.username}' != user.username:
            if user.username is None:
                return
            await users_dal.update_user(chat_id=event.from_user.id, username=f'@{event.from_user.username}')

        return await handler(event, data)
