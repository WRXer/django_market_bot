import locale
import telebot
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')    #Установка локали на русский язык

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    """
    Стартовый обработчик
    :param message:
    :return:
    """
    pass
