from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import MenuItem
from django.db.models import Q
from .models import Order
import uuid
from django.utils import timezone

def view_login(request):
    template = loader.get_template('login.html')
    context = {
        'login_page': 'login',
    }
    return HttpResponse(template.render(context, request))

def view_index(request):
    template = loader.get_template('index.html')
    context = {
        'index_page': 'index',
    }
    return HttpResponse(template.render(context, request))

def view_signup(request):
    template = loader.get_template('signup.html')
    context = {
        'signup_page': 'signup',
    }
    return HttpResponse(template.render(context, request))

def dashboard_view(request):
    template = loader.get_template('dashboard.html')
    context = {
        'dashboard_page': 'dashboard',
    }
    return HttpResponse(template.render(context, request))

def menu_view(request):
    template = loader.get_template('menu.html')
    context = {
        'menu_page': 'menu',
    }
    return HttpResponse(template.render(context, request))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other desired page
        else:
            error_message = 'Invalid credentials'  # Error message to display if authentication fails
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Additional validation checks can be performed here
        
        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
    else:
        return render(request, 'signup.html')
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def menu_view(request):
    query = request.GET.get('q')
    if query:
        menu_items = MenuItem.objects.filter(Q(title__icontains=query) | Q(category__icontains=query))
    else:
        menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items, 'search_query': query})

def order_view(request):
    item_name = request.GET.get('item_name')
    quantity = request.GET.get('quantity')
    template = loader.get_template('order.html')
    context = {
        'order_page': 'order',
        'item_name': item_name,
        'quantity': quantity,
    }
    return HttpResponse(template.render(context, request))


def place_order_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        item_name = request.POST['item_name']
        quantity = request.POST['quantity']
        address = request.POST['address']

        # Generate a unique order ID
        order_id = generate_unique_order_id()

        # Create a new order object and save it to the database
        order = Order(order_id=order_id, name=name, email=email, phone=phone, item_name=item_name, quantity=quantity, address=address)
        order.save()

        # Store the order ID in the session
        request.session['order_id'] = order_id

        # Redirect to a success page or any other desired page
        return redirect('order_success')

    return HttpResponseBadRequest('Invalid request')

def generate_unique_order_id():
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_string = str(uuid.uuid4()).replace('-', '')[:6]
    order_id = f'{timestamp}-{random_string}'
    return order_id

def order_success(request):
    return render(request, 'order_success.html')


def rate_order(request):
    if request.method == 'POST':
        star_rating = request.POST.get('rating')
        order_id = request.session.get('order_id')  # Retrieve the order ID from the session
        try:
            order = Order.objects.get(order_id=order_id)  # Get the order object
            order.star_rating = star_rating  # Assign the rating to the order
            order.save()  # Save the order
        except Order.DoesNotExist:
            # Handle the case if the order does not exist
            return HttpResponseBadRequest('Invalid order')
        
        return redirect('dashboard')  # Redirect to a 'thank you' page or another appropriate URL
    else:
        return redirect('order')  # Redirect back to the order page if accessed directly without submission

