from datetime import datetime, timedelta
from ..vpn.protocol.reused import display_payment_method_message
from src.core import settings
from src.database import users_dal, xui_configs_api, priz_dal
from .markup import menu_markup
from aiogram import types, filters
import asyncio

def get_design():
    emoji_mapping = {
        '☃️': [1, 2, 12],
        '🌱': [3, 4, 5],
        '🏖': [6, 7, 8],
        '🍂': [9, 10, 11]
    }
        
    time_greetings = {
        (5, 12): "Доброго утра",
        (12, 17): "Доброго дня",
        (17, 21): "Доброго вечера",
    }
    
    msk_time = datetime.now() + timedelta(hours=3)
    current_month = msk_time.month
    current_hour = msk_time.hour
    
    emoji = next(emoji for emoji, months in emoji_mapping.items() if current_month in months)
    time_of_day = next((greeting for (start, end), greeting in time_greetings.items() if start <= current_hour < end), "Доброй ночи")
    return emoji, time_of_day


def get_greeting_messages(hello_message: bool):
    if hello_message:
        return (
            'CAACAgQAAxkBAAIERme8tRGuVUnVkllFTaYvWHKRa8e1AAJFFwAC-OdhUS4TXEGyMqfeNgQ',
            'Добро пожаловать в экосистему <a href="https://t.me/radjanews"><b>Radja Service</b></a>!\nСпасибо за то, что пользуетесь нашими сервисами! 🥹'
        )
    return ('CAACAgQAAxkDAAIDIme2t91OrpHYvQFSCoW56IxJoAOKAAKBFwACxY1hUSH7bxr0PHQ-NgQ', None)


def get_menu_text(first_name: str, emoji: str, time_of_day: str) -> str:
    return (f'<a href="https://t.me/radjanews">{emoji}</a> {time_of_day}, <b>{first_name}</b>\n\n'
            '<a href="https://telegra.ph/Nashi-preimushchestva-04-05"><b>🥇 Наши преимущества</b></a>\n'
            '<a href="https://t.me/radjafeedback"><b>💭 Отзывы клиентов</b></a>\n'
           )
    
    
def get_text_for_referral_owner(event: types.Message) -> str:
    return f'🔔 У вас новый реферал!\n<b>@{event.from_user.username}</b>'


async def process_referral_owner_chat_id(event: types.Message, args: str, referral_owner_chat_id: int):
    referral_owner = await users_dal.get_user(chat_id=referral_owner_chat_id)
    
    if referral_owner:
        text = get_text_for_referral_owner(event)
        
        await display_message_for_referral_owner(event=event, referral_owner_chat_id=referral_owner_chat_id, text=text)
        
        user = await users_dal.get_user(chat_id=event.from_user.id)
        
        if not user.referral_owner_chat_id or user.referral_owner_chat_id != referral_owner_chat_id:
            await users_dal.update_user(chat_id=event.from_user.id, referral_owner_chat_id=referral_owner_chat_id, data_inviting=int(datetime.now().timestamp()))
            
            referrals = await users_dal.get_users(referral_owner_chat_id=referral_owner_chat_id)
            referral_count = len(referrals)
            referral_lvls = settings.referral_lvls
            referral_level = 0

            for lvl, threshold in enumerate(referral_lvls, start=1):
                if referral_count >= threshold:
                    referral_level = lvl
            
            if referral_level > 0:
                sent_message = await event.bot.send_message(
                    chat_id=referral_owner_chat_id,
                    text='Поздравляем, вы достигли нового реферального уровня!\n<b>Перейдите в раздел <i>„🫂 Реферальная система“</i>, '
                    'чтобы забрать свою награду!</b>' 
                )
                await priz_dal.add_priz(chat_id=referral_owner_chat_id, lvl=referral_level)
                asyncio.create_task(delete_message_after_delay(event.bot, referral_owner_chat_id, sent_message.message_id, 60))
        else:
            print(f"Пользователь {event.from_user.first_name} уже добавлен как реферал для владельца с chat_id={referral_owner_chat_id}")
    else:
        print(f"Ошибка: владелец с chat_id={referral_owner_chat_id} не найден.")

        
async def display_message_for_referral_owner(event: types.Message, referral_owner_chat_id: int, text: str):
    sent_message = await event.bot.send_message(
        chat_id=referral_owner_chat_id,
        text=text
    )
    
    asyncio.create_task(delete_message_after_delay(event.bot, referral_owner_chat_id, sent_message.message_id, 30))

async def delete_message_after_delay(bot, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def display_response_for_deeplink_with_protocol(event: types.Message, args: str):
    protocol = args
    await display_payment_method_message(event=event, protocol=protocol, send=True)
    return

async def display_response_for_deeplink_with_referral_owner_chat_id(event: types.Message, args: str):
    referral_owner_chat_id = int(args)
            
    if event.from_user.id != referral_owner_chat_id: 
        await process_referral_owner_chat_id(event=event, args=args, referral_owner_chat_id=referral_owner_chat_id)


async def interaction_with_deeplink(event: types.Message, command: filters.CommandObject):
    args = command.args
    
    if not args.isdigit():
        await event.delete()
        await display_response_for_deeplink_with_protocol(event=event, args=args)
    else:
        referral_owner_chat_id = int(args)
        user = await users_dal.get_user(chat_id=event.from_user.id)

        if user and user.referral_owner_chat_id:
            return

        await display_response_for_deeplink_with_referral_owner_chat_id(event=event, args=args)


async def display_menu_messages(event: types.Message | types.CallbackQuery, hello_message: bool = False, edit: bool = False, sticker_status: bool = None, command: filters.CommandObject = None):
    if command:
        if command.args:
            await interaction_with_deeplink(event=event, command=command)
            if not command.args.isdigit():
                return 
            
    emoji, time_of_day = get_design()
    sticker, welcome_message = get_greeting_messages(hello_message)
    chat_id = event.from_user.id
    message_id = event.message.message_id if edit else None
    
    if sticker_status == None and not message_id:
        await event.bot.send_sticker(chat_id=chat_id, sticker=sticker)
    
    if welcome_message:
        await event.bot.send_message(chat_id=chat_id, text=welcome_message, disable_web_page_preview=True)
    
    welcome_text = get_menu_text(event.from_user.first_name, emoji, time_of_day)
    result = await xui_configs_api.get_configs(chat_id=event.from_user.id)

    if message_id is not None:
        await event.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=welcome_text,
            reply_markup=await menu_markup(result=result),
            disable_web_page_preview=True
        )
    else:
        await event.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=await menu_markup(result=result),
            disable_web_page_preview=True
        )
