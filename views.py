import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password.'
    return render(request, 'login.html', {'error': error})

@login_required
def dashboard(request):
    # Fetch e-commerce data from Fake Store API
    products = requests.get('https://fakestoreapi.com/products').json()
    carts = requests.get('https://fakestoreapi.com/carts').json()

    # Simple analytics
    total_products = len(products)
    total_orders = len(carts)

    # Calculate total revenue from carts and product prices
    product_price = {item['id']: item['price'] for item in products}
    total_revenue = 0
    for cart in carts:
        for item in cart['products']:
            pid, qty = item['productId'], item['quantity']
            price = product_price.get(pid, 0)
            total_revenue += price * qty

    # Top 5 most expensive products
    top_products = sorted(products, key=lambda x: x['price'], reverse=True)[:5]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2),
        'top_products': top_products,
        'products': products,
        'carts': carts,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)

@login_required
def home(request):
    # These would typically come from your database or the API
    categories = [
        {'name': 'Watch', 'image_url': '/static/livedb/cat-watch.jpg', 'product_count': 17},
        {'name': 'Fashionista', 'image_url': '/static/livedb/cat-fashion.jpg', 'product_count': 8},
        # ...more categories
    ]
    popular_products = [
        {'title': 'Longines Watch Tradition', 'image': '/static/livedb/prod-watch.jpg', 'price': 222},
        {'title': 'Cody & Wendy Large Scarf', 'image': '/static/livedb/prod-scarf.jpg', 'price': 16},
        # ... top 6-8 products
    ]
    return render(request, 'home.html', {
        'categories': categories,
        'popular_products': popular_products,
    })

def logout_view(request):
    logout(request)
    return redirect('login')
