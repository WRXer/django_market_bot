from channels.db import database_sync_to_async

from market.models import TelegramUser, Category, SubCategory


@database_sync_to_async
def get_or_create_user(user_id):
    """
    Получение или создалние пользователя
    :param user_id:
    :return:
    """
    return TelegramUser.objects.get_or_create(telegram_id=user_id)[0]

@database_sync_to_async
def get_categories():
    """
    Получение категорий товара
    :param user_id:
    :return:
    """
    return list(Category.objects.all())

@database_sync_to_async
def get_subcategories(category_id):
    """
    Получение категорий товара
    :param user_id:
    :return:
    """
    return list(SubCategory.objects.filter(category_id=category_id))
