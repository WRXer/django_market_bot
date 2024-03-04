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