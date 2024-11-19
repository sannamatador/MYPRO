from django.contrib import admin
from .models import Product, Order, User


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'quantity')  # Убедитесь, что вы добавили нужные поля


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(User)


# Register your models here.
