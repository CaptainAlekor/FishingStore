from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
import logging
import asyncio
from asgiref.sync import sync_to_async

from .models import *

logger = logging.getLogger('main')


def registerPage(request):
    logger.info('Now on registration page (views.py registerPage)')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    logger.info('Now on login page (views.py loginPage)')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logger.info('User logged out (views.py logoutUser)')
    logout(request)
    return redirect('login')


@sync_to_async
def get_products():
    products = Product.objects.all()
    return products


@sync_to_async
def get_customer(user, name, email):
    customer = Customer.objects.get_or_create(
        user=user,
        name=name,
        email=email
    )
    return customer


@sync_to_async
def get_order(customer, complete):
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=complete
    )
    return order


def store(request):
    logger.info('Now on store page (views.py store)')

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except:
            customer = asyncio.run(get_customer(
                request.user,
                request.user.username,
                request.user.email
            ))
        order = asyncio.run(get_order(customer, False))
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = asyncio.run(get_products())
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    logger.info('Now on cart page (views.py cart)')

    if request.user.is_authenticated:
        customer = request.user.customer
        order = asyncio.run(get_order(customer, False))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    logger.info('Now on checkout page (views.py checkout)')
    if request.user.is_authenticated:
        customer = request.user.customer
        order = asyncio.run(get_order(customer, False))
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


@sync_to_async
def get_product_by_id(prod_id):
    products = Product.objects.get(id=prod_id)
    return products


@sync_to_async
def get_order_item(order, product):
    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
        )
    return orderItem


def updateItem(request):
    logger.info('Updating items... (views.py updateItem)')
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = asyncio.run(get_product_by_id(productId))
    order = asyncio.run(get_order(customer, False))

    orderItem = asyncio.run(get_order_item(order, product))

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    logger.info('Items updated (views.py updateItem)')
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    logger.info('Processing order... (views.py processOrder)')
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = asyncio.run(get_order(customer, False))
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
            logger.info('Updating items... (views.py updateItem)')
    else:
        logger.info('User is not logged in... (views.py updateItem)')

    return JsonResponse('Payment complete', safe=False)
