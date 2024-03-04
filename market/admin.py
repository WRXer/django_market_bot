from django.contrib import admin
from market.models import TelegramUser


# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
