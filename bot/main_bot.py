import asyncio
import locale
import telebot
import os
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from bot.database_sync import get_or_create_user, get_categories, get_subcategories, get_products, get_product
from bot.views import is_user_subscribed


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')    #Установка локали на русский язык

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='HTML')
telebot.logger.setLevel(settings.LOG_LEVEL)
user_state = {}

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
async def main_handler(callback):
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
async def catalog_handler(callback):
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

@bot.callback_query_handler(func=lambda callback: callback.data.startswith("category_"))
async def category_handler(callback):
    """
    Обработка кнопки категории(вывод подкатегорий)
    :param callback:
    :return:
    """
    user_state[callback.from_user.id] = {}
    category_id = int(callback.data.split('_')[1])
    user_state[callback.from_user.id]["category_id"] = category_id    #Запоминаем категорию, выбранную пользователем
    subcategories = await get_subcategories(category_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for subcategory in subcategories:
        keyboard.add(types.InlineKeyboardButton(text=subcategory.name, callback_data=f"subcategory_{subcategory.id}"))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data='catalog'))
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Выберите подкатегорию:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith("subcategory_"))
async def subcategory_handler(callback):
    """
    Обработка кнопки подкатегории(вывод продуктов)
    :param callback:
    :return:
    """
    try:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    except Exception as e:
        print(f"Ошибка удаления сообщения: {e}")
    subcategory_id = int(callback.data.split('_')[1])
    user_state[callback.from_user.id]["subcategory_id"] = subcategory_id
    products = await get_products(subcategory_id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for product in products:
        keyboard.add(types.InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}"))
    keyboard.add(types.InlineKeyboardButton("Назад", callback_data=f'category_{user_state[callback.from_user.id]["category_id"]}'))    #Кнопка для возврата в список подкатегорий
    await bot.send_message(chat_id=callback.message.chat.id, text="Выберите продукт:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith("product_"))
async def subcategory_handler(callback):
    """
    Обработка кнопки выбора определенного продукта
    :param callback:
    :return:
    """
    try:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    except Exception as e:
        print(f"Ошибка удаления сообщения: {e}")
    product_id = int(callback.data.split('_')[1])
    product = await get_product(product_id)
    try:
        if product.photo:
            photo_path = f"{product.photo}"
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(types.InlineKeyboardButton(text="Добавить в корзину", callback_data="quantity"))
            keyboard.add(types.InlineKeyboardButton("Назад", callback_data=f'subcategory_{user_state[callback.message.chat.id]["subcategory_id"]}'))
            await bot.send_photo(photo=open(photo_path, 'rb'), chat_id=callback.message.chat.id, caption=f"Выбран продукт: \n{product.name}\n{product.description}", reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(types.InlineKeyboardButton(text="Добавить в корзину", callback_data="quantity"))
            keyboard.add(types.InlineKeyboardButton("Назад", callback_data=f'subcategory_{user_state[callback.message.chat.id]["subcategory_id"]}'))
            await bot.send_message(chat_id=callback.message.chat.id, text=f"Выбран продукт: \n{product.name}\n{product.description}\nФото отсутствует", reply_markup=keyboard)
    except Exception as e:
        print(f"Ошибка отправки изображения: {e}")





