from channels.db import database_sync_to_async

from market.models import TelegramUser, Category, SubCategory, Product, Cart


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

@database_sync_to_async
def get_products(subcategory_id):
    """
    Получение продукта
    :param user_id:
    :return:
    """
    return list(Product.objects.filter(subcategory_id=subcategory_id))

@database_sync_to_async
def get_product(product_id):
    """
    Получение выбранного продукта
    :param user_id:
    :return:
    """
    return Product.objects.get(id=product_id)

@database_sync_to_async
def record_to_cart(user, product, quantity):
    """
    Добавление выбранного продукта в корзину
    :param user:
    :return:
    """
    #existing_item = Cart.objects.filter(user=user,product=product).first()
    if Cart.objects.filter(user=user.id,product=product.id).first():
        existing_item = Cart.objects.filter(user=user.id, product=product.id).first()
        existing_item.quantity += quantity    #Обновляем количество товара, если уже есть в корзине
        existing_item.save()
    else:
        return Cart.objects.create(user=user, product=product, quantity=quantity)

@database_sync_to_async
def get_list_cart(user):
    """
    Получение списка корзины
    :param user:
    :return:
    """
    list_cart = list(Cart.objects.filter(user=user))
    print(f"Пользователь {user} зашел в корзину. {list_cart}")
    return list_cart

@database_sync_to_async
def get_cart_product(user, cart_product_id):
    """
    Получение данных продукта из корзины
    :param user:
    :return:
    """
    cart_product = Cart.objects.filter(user=user.id, product=cart_product_id).first()
    print(cart_product)
    return cart_product

@database_sync_to_async
def removing_product(user, cart_product_id):
    """
    Удаление выбранного продукта из корзины
    :param user:
    :param cart_product_id:
    :return:
    """
    cart_product = Cart.objects.filter(user=user.id, product=cart_product_id).first()
    cart_product.delete()
