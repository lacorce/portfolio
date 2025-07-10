from .user import UsersDal, PrizDal
from .api import XUIConfigsAPI
from .payment import PaymentTransactionsDal
from .base import Database


db = Database()

users_dal = UsersDal(db=db)
xui_configs_api = XUIConfigsAPI(db=db)
payment_transactions_dal = PaymentTransactionsDal(db=db)
priz_dal = PrizDal(db=db)
