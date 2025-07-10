from ..base import Database
from ..models import PaymentTransactionModel

from typing import Any, Optional
from sqlalchemy import select, insert, update


class PaymentTransactionsDal:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_payment_transaction(self, invoice_id: str, chat_id: int, payment_method: str, protocol: str, config_keys: list, amount_value: float, key_count: int, month_count) -> None:
        statement = insert(PaymentTransactionModel).values(
            id=invoice_id,
            chat_id=chat_id,
            payment_method=payment_method,
            protocol=protocol,
            config_keys=config_keys,
            amount_value=amount_value,
            key_count=key_count,
            month_count=month_count
        )
        
        await self.db.execute(statement=statement)
        
    async def get_payment_transaction(self, **kwargs: Any) -> PaymentTransactionModel:
        statement = select(PaymentTransactionModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='one')
        
    async def get_payment_transactions(self, **kwargs: Any) -> PaymentTransactionModel:
        statement = select(PaymentTransactionModel).filter_by(**kwargs)
        
        return await self.db.execute(statement=statement, fetch='all')

    async def update_payment_transaction(self, invoice_id: str, **kwargs: Any) -> None:
        statement = update(PaymentTransactionModel).where(
            PaymentTransactionModel.id==invoice_id,
        ).values(**kwargs)
        
        return await self.db.execute(statement=statement)
