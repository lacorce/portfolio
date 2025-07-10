from src.middlewares import ExistsMiddleware, SubscribeMiddleware

from aiogram import Router
from fastapi import APIRouter


cryptopay_router = APIRouter()
yookassa_router = APIRouter()

user_router = Router()
user_router.message.outer_middleware(ExistsMiddleware())
user_router.message.outer_middleware(SubscribeMiddleware())
user_router.callback_query.outer_middleware(SubscribeMiddleware())
