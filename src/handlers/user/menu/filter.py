from src.database import users_dal

from aiogram import filters, types
    
class HelloMessageFilter(filters.BaseFilter):
    async def __call__(self, message: types.Message):
        chat_id = message.from_user.id 
        user = await users_dal.get_user(chat_id=chat_id)

        if not user.hello_message:
            await users_dal.update_user(chat_id=chat_id, hello_message=True)
            return True 
            
        return False
    
class IsTopic(filters.BaseFilter):
    def __init__(self, topic_id: int, chat_id: int):
        self.topic_id = topic_id
        self.chat_id = chat_id

    async def __call__(self, message: types.Message):
        if message.chat.type == "private":
            return False

        if int(message.chat.id) == int(self.chat_id):
            if hasattr(message, 'message_thread_id'):
                if int(message.message_thread_id) == int(self.topic_id):
                    return True
        return False


class IsEmptyDeepLinkWithReferralOwnerChatIDFilter(filters.BaseFilter):
    async def __call__(self, message: types.Message):
        if len(message.text.split(' ')[0]) == 6: 
            referral_owner_chat_id = message.text.split(' ')[1]
        
        await message.answer(text=f'{referral_owner_chat_id}')
        
        return True
