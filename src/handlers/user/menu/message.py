from src.core.routes import user_router
from src.core import settings

from .filter import HelloMessageFilter, IsEmptyDeepLinkWithReferralOwnerChatIDFilter, IsTopic
from .reused import display_menu_messages
from .markup import controls_markup

from aiogram import filters, types
from aiogram.filters import CommandObject


@user_router.message(HelloMessageFilter(), filters.CommandStart())
async def hello_message_filter_handler(message: types.Message, command: CommandObject):

    await display_menu_messages(event=message, hello_message=True, command=command)


@user_router.message(IsTopic(topic_id=settings.topic_vpn_id, chat_id=settings.supergroup_id), filters.CommandStart())
async def topic_filter_handler(message: types.Message):
    await message.answer("<b>Меню управления RADJA VPN</b>",
                        reply_markup=await controls_markup())


@user_router.message(filters.CommandStart())
async def start_command_handler(message: types.Message, command: CommandObject):
    await display_menu_messages(event=message, command=command)
    