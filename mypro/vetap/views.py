from django.shortcuts import render, redirect
from django.contrib.auth import login
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
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return render(request, 'vetapp/login.html', {'error': 'Пользователь не найден.'})
        username = user.first_name
        return render(request, 'vetapp/success1.html', {'first_name': username})
    return render(request, 'vetapp/login.html')


def user_logout(request):
    request.session.flush()
    return redirect('main')


def product(request):
    products = Product.objects.all()
    return render(request, 'vetapp/product.html', {'products': products})


def order_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(user=user)
    return render(request, 'vetapp/order.html', {'orders': orders})
