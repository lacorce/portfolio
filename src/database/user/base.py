from ..base import Database
from ..models import UsersModel, Transactions

from typing import Any
from sqlalchemy import select, insert, update, delete


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

class TransactionsDal:
    def __init__(self, db: Database):
        self.db = db

    async def add_transaction(
        self, 
        chat_id: int, 
        type_: str, 
        amount: int, 
        currency: str, 
        created_at: int = None
    ) -> None:
        values = {
            "chat_id": chat_id,
            "type": type_,
            "amount": amount,
            "currency": currency,
        }
        if created_at is not None:
            values["created_at"] = created_at
        
        statement = insert(Transactions).values(**values)
        await self.db.execute(statement=statement)

    async def get_transaction(self, **kwargs: Any) -> Transactions:
        statement = select(Transactions).filter_by(**kwargs)
        return await self.db.execute(statement=statement, fetch="one")

    async def get_transactions(self, **kwargs: Any) -> Transactions:
        statement = select(Transactions).filter_by(**kwargs)
        return await self.db.execute(statement=statement, fetch="all")

    async def update_transaction(self, transaction_id: int, **kwargs: Any) -> None:
        statement = update(Transactions).where(
            Transactions.id == transaction_id
        ).values(**kwargs)
        await self.db.execute(statement=statement)

    async def delete_transaction(self, transaction_id: int) -> None:
        statement = delete(Transactions).where(Transactions.id == transaction_id)
        await self.db.execute(statement=statement)

    async def get_transactions_by_period(self, user_id: int, start_ts: int, end_ts: int):
        statement = select(Transactions).where(
        Transactions.chat_id == user_id,
        Transactions.created_at >= start_ts,
        Transactions.created_at <= end_ts,
    )
        return await self.db.execute(statement=statement, fetch="all")