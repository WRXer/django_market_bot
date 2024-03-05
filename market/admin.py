from django.contrib import admin
from market.models import TelegramUser, Product, SubCategory, Category


# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
