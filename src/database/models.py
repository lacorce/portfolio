from datetime import datetime 

from typing import Annotated

from sqlalchemy import BigInteger, func, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]


class Base(DeclarativeBase): 
    pass

class UsersModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(default=False)
    hello_message: Mapped[bool] = mapped_column(default=False)
    trial_period: Mapped[bool] = mapped_column(default=False)
    referral_owner_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)
    data_inviting: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)

class PrizModel(Base):
    __tablename__ = 'prizes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    lvl: Mapped[int]
    status: Mapped[int] = mapped_column(default=0)

class XUIConfigModel(Base):
    __tablename__ = 'xui_configs'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=False)
    client_id: Mapped[str]
    config_key: Mapped[str]
    expires_time: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[int] = mapped_column(BigInteger, default=int(datetime.now().timestamp()))
    
class PaymentTransactionModel(Base):
    __tablename__ = 'payment_transactions'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    payment_method: Mapped[str]
    protocol: Mapped[str]
    config_keys: Mapped[list] = mapped_column(JSON)
    amount_value: Mapped[float]
    key_count: Mapped[int]
    month_count: Mapped[int]
    status: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[int] = mapped_column(BigInteger, default=int(datetime.now().timestamp()))