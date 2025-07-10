from .user import UsersDal, TransactionsDal
from .base import Database

db = Database()

users_dal = UsersDal(db=db)
transactions_dal = TransactionsDal(db=db)