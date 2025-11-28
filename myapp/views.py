from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem


# ---------- Home, About, Contact ----------
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# ---------- User List ----------
def users_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

# ---------- Menu ----------
def menu(request):
    cart_items = request.session.get('cart', [])
    total = sum(item['price']*item['quantity'] for item in cart_items)
    return render(request, 'menu.html', {'cart_items': cart_items, 'total': total})

# ---------- Signup ----------
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST.get('first_name', '')
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                password=password1
            )
            messages.success(request, "Account created successfully!")
            return redirect('login')

    return render(request, 'signup.html')

# ---------- Login ----------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

# ---------- Logout ----------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

# ---------- Billing ----------
def billing(request):
    cart_items = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # 1️⃣ Save order to DB
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=name, 
            email=email,
            phone=phone,
            address=address,
            total=total
        )

        # 2️⃣ Save each cart item to OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )

        # 3️⃣ Clear cart
        request.session['cart'] = []

        # Optional: save order ID to session to use in order_success page
        request.session['last_order_id'] = order.id

        return redirect('order_success')

    return render(request, 'billing.html', {'cart_items': cart_items, 'total': total})

# ---------- Order Success ----------
def order_success(request):
    last_order_id = request.session.get('last_order_id')
    last_order = None
    if last_order_id:
        last_order = Order.objects.filter(id=last_order_id).first()
        # Clear it after displaying
        del request.session['last_order_id']

    return render(request, 'order_success.html', {'last_order': last_order})

# ---------- Order History ----------
def order_history(request):
    if request.user.is_authenticated:
        history = Order.objects.filter(user=request.user).order_by('-id')
    else:
        history = []
    return render(request, 'order_history.html', {'history': history})

