from telebot.types import ChatMember
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings


bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')

async def is_user_subscribed(user_id, chatid):
    """
    Проверка на подписку в канале
    :param user_id:
    :param chat_id:
    :return:
    """
    try:
        chat_id = f"@{chatid}"
        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return False


