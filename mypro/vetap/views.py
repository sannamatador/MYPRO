from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Product, Order


def main(request):
    return render(request, 'vetapp/base.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'vetapp/register.html', {'error': 'Пользователь с таким email уже существует.'})
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.save()
        return render(request, 'vetapp/success.html', {'first_name': first_name})
    return render(request, 'vetapp/register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()  # Получаем email из формы

        # Проверяем существование пользователя
        user = User.objects.filter(email=email)
        if user.exists():  # Проверяем, существует ли пользователь
            user = user.first()  # Получаем первого пользователя
            request.session['user_id'] = user.id  # Сохраняем идентификатор пользователя в сессии
            return render(request, 'vetapp/success1.html', {'first_name': user.first_name})  # Успешный вход
        else:
            # Обработка случая, когда пользователь не найден
            return render(request, 'vetapp/login.html', {'error': 'Пользователь с таким email не найден.'})

    # Если метод не POST, просто возвращаем страницу входа
    return render(request, 'vetapp/login.html')


def user_logout(request):
    request.session.flush()
    return redirect('main')


def product(request):
    products = Product.objects.all()
    return render(request, 'vetapp/product.html', {'products': products})


def order_view(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Если пользователь не авторизован, перенаправляем на страницу входа

    user = get_object_or_404(User, id=request.session['user_id'])  # Получаем пользователя
    cart = request.session.get('cart', {})  # Получаем корзину из сессии

    # Получаем информацию о товарах в корзине
    order_items = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        order_items.append({'product': product, 'quantity': quantity})  # Формируем список с товарами и их количеством

    return render(request, 'vetapp/order_view.html', {
        'user': user,
        'order_items': order_items  # Передаем список товаров в шаблон
    })


def order_create(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        cart = request.session.get('cart', {})  # Получаем корзину из сессии

        if not cart:
            messages.error(request, "Корзина пуста! Добавьте товары перед оформлением заказа.")
            return redirect('product')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)

            if quantity > product.quantity:  # Проверка наличия товара
                messages.error(request, f"Недостаточно товара: {product.name}")
                return redirect('product')

            # Создаем новый заказ
            order = Order(
                user=user,
                product=product,
                quantity=quantity,
                status='completed'
            )
            order.save()

        # Очищаем корзину после оформления заказа
        del request.session['cart']
        messages.success(request, "Ваш заказ оформлен! Спасибо за покупку.")
        return redirect('order_create')  # Перенаправляем на просмотр заказов

    return redirect('product')  # Возвращаем, если метод не POST


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Получаем товар по ID

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Получаем количество из формы, по умолчанию 1
        if quantity < 1:
            quantity = 1  # Убедимся, что количество положительное

        cart = request.session.get('cart', {})  # Получаем корзину из сессии или создаем новую
        if product_id in cart:
            cart[product_id] += quantity  # Увеличиваем количество, если товар уже есть в корзине
        else:
            cart[product_id] = quantity  # Добавляем товар в корзину

        request.session['cart'] = cart  # Сохраняем корзину обратно в сессию

        messages.success(request, f'{product.name} добавлен в корзину!')  # Сообщаем об успехе
        return redirect('product')  # Возвращаем на страницу с товарами

    return redirect('product')  # Если GET-запрос, возвращаем на страницу
