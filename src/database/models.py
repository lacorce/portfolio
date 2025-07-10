from datetime import datetime 

from typing import Annotated

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]


class Base(DeclarativeBase): 
    pass

class UsersModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(default=False)
    base_currency : Mapped[str] = mapped_column(default=False)   
    created_at: Mapped[int] = mapped_column(BigInteger, server_default=func.strftime('%s','now'))

class Transactions(Base):
    __tablename__ = 'transactions'

    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    type: Mapped[str] = mapped_column(default=False)
    amount: Mapped[int] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(default=False)
    created_at: Mapped[int] = mapped_column(BigInteger)