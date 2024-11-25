from django.contrib import admin
from .models import Product, Order, User

admin.site.register(Product) # Регистрация моделей в админ-панели
admin.site.register(Order)
admin.site.register(User)


# Register your models here.
