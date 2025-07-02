from aiogram import Router
from src.middlewares import ExistsMiddleware

user_rou = Router()
user_rou.message.outer_middleware(ExistsMiddleware())
admin_rou = Router()