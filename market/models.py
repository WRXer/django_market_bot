from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    """
    Класс Пользователь для связи с айди ТГ
    """
    telegram_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя в Telegram")

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

class Category(models.Model):
    """
    Класс категории товаров
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегория"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True, verbose_name="Фото товара")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Подкатегория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукт"

class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product}: {self.quantity}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"