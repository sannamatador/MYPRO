from django.db import models


class User(models.Model): # Модель пользователя
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model): # Модель товара
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)  # Количество на складе
    status = models.CharField(max_length=20, choices=[
        ('available', 'Доступен'),
        ('unavailable', 'Недоступен')
    ], default='available')

    def __str__(self):
        return self.name


class Order(models.Model):  #Модель заказа
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('completed', 'Завершен'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Удалено default=1
    quantity = models.PositiveIntegerField(default=1)  # Количество
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Общая цена

    def __str__(self):
        return f"Order {self.id} by {self.user.first_name} - Status: {self.status}"

