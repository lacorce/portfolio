from ..base import Database
from ..models import UsersModel, PrizModel

from typing import Any, Optional
from sqlalchemy import select, insert, update


class UsersDal:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_user(self, chat_id: int, username: str) -> None:
        statement = insert(UsersModel).values(
            chat_id=chat_id,
            username=username
        )
        
        await self.db.execute(statement=statement)
        
    async def get_user(self, **kwargs: Any) -> UsersModel:
        statement = select(UsersModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='one')
        
    async def get_users(self, **kwargs: Any) -> UsersModel:
        statement = select(UsersModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='all')

    async def update_user(self, chat_id: int, **kwargs: Any) -> None:
        statement = update(UsersModel).where(
            UsersModel.chat_id==chat_id,
        ).values(**kwargs)
        
        return await self.db.execute(statement=statement)
    
class PrizDal:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_priz(self, chat_id: int, lvl: int) -> None:
        statement = insert(PrizModel).values(
            chat_id=chat_id,
            lvl=lvl
        )
        
        await self.db.execute(statement=statement)
        
    async def get_priz(self, **kwargs: Any) -> PrizModel:
        statement = select(PrizModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='one')

    async def get_prizs(self, **kwargs: Any) -> PrizModel:
        statement = select(PrizModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='all')
    
    async def update_priz(self, chat_id: int, **kwargs: Any) -> None:
        statement = update(PrizModel).where(
            PrizModel.chat_id==chat_id,
        ).values(**kwargs)
        
        return await self.db.execute(statement=statement)
    
    async def update_priz_by_id(self, priz_id: int, status: int):
        statement = update(PrizModel).where(PrizModel.id == priz_id).values(status=status)
        await self.db.execute(statement)
        await self.db.execute(statement=statement)

