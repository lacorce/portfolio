from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.database import get_user, add_user, update_username

class ExistsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = await get_user(chat_id=event.from_user.id)
        if not user:
            await add_user(chat_id=event.from_user.id, username=f'@{event.from_user.username}')
            user = await get_user(chat_id=event.from_user.id)

        if f'@{event.from_user.username}' != user[2]:
            if user[2] is None:
                return
            await update_username(chat_id=event.from_user.id, username=f'@{event.from_user.username}')

        return await handler(event, data)
