import asyncio
import locale
import telebot
import os
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from bot.database_sync import get_or_create_user, get_categories
from bot.views import is_user_subscribed


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
    user_id = message.from_user.id
    chat_id = os.getenv('CHANEL_ID')
    telegram_user = await get_or_create_user(user_id)
    if await is_user_subscribed(user_id, chat_id):    # Пользователь подписан, отправляем приветственное сообщение с клавиатурой
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button_catalog =types.InlineKeyboardButton("Каталог", callback_data='catalog')
        button_my_cart = types.InlineKeyboardButton("Моя корзина", callback_data='my_cart')
        button_faq = types.InlineKeyboardButton("FAQ", callback_data='faq')
        keyboard.add(button_catalog, button_my_cart, button_faq)
        await bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)    #Отправляем приветственное сообщение с клавиатурой



    else:    # Пользователь не подписан, отправляем сообщение с предложением подписаться
        keyboard = types.InlineKeyboardMarkup()
        subscribe_button = types.InlineKeyboardButton("Подписаться", url=f"https://t.me/{chat_id}")
        button_start = types.InlineKeyboardButton("Продолжить", callback_data="start")
        keyboard.add(subscribe_button, button_start)
        await bot.send_message(message.chat.id,"Для использования бота, подпишитесь на наш канал.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data == "start")
async def query_handler(callback):
    user_id = callback.from_user.id
    chat_id = os.getenv('CHANEL_ID')
    if await is_user_subscribed(user_id, chat_id):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button_catalog = types.InlineKeyboardButton("Каталог", callback_data='catalog')
        button_my_cart = types.InlineKeyboardButton("Моя корзина", callback_data='my_cart')
        button_faq = types.InlineKeyboardButton("FAQ", callback_data='faq')
        keyboard.add(button_catalog, button_my_cart, button_faq)
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите действие:", reply_markup=keyboard)    #Отправляем приветственное сообщение с клавиатурой
    else:
        message = await bot.send_message(callback.message.chat.id, text="Вы все еще не подписаны. Пожалуйста, подпишитесь наш канал.")
        await asyncio.sleep(5)     #Удаление сообщения после определенного времени
        await bot.delete_message(callback.message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda callback: callback.data == "catalog")
async def query_handler(callback):
    """
    Обработка кнопки каталог(вывод категорий)
    :param callback:
    :return:
    """
    categories = await get_categories()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for category in categories:
        keyboard.add(types.InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='start'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите категорию:", reply_markup=keyboard)
