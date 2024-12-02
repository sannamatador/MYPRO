import time
from django.test import TestCase
from vetap.models import User, Product, Order


class PerformanceTests(TestCase):

    def setUp(self):
        # Создаем тестового пользователя и продукт для использования в тестах
        self.user = User.objects.create(first_name='testuser_fn', last_name='testuser_sn', email='test1@example.com')
        self.product = Product.objects.create(name='Test Product', price=10.99)

    def test_user_performance(self):
        start_time = time.perf_counter()
        User.objects.create(first_name='testuser_fn2', last_name='testuser_sn2', email='test2@example.com')
        print(f"User  creation time: {(time.perf_counter() - start_time):.6f} seconds")

    def test_product_performance(self):
        start_time = time.perf_counter()
        Product.objects.create(name='Test Product 2', price=20.99)
        print(f"Product creation time: {(time.perf_counter() - start_time):.6f} seconds")

    def test_order_performance(self):
        start_time = time.perf_counter()
        Order.objects.create(user=self.user, product=self.product, quantity=1)
        print(f"Order creation time: {(time.perf_counter() - start_time):.6f} seconds")
