import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from orders.models import TelegramUser

from django.conf import settings


order_number = None


def send_order_to_telegram(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        region = request.POST.get('region')
        city = request.POST.get('city')
        new_post_branch = request.POST.get('new_post_branch')
        order_note = request.POST.get('order_note')

        # Get the cart_id from the session
        cart_id = request.session.session_key

        if not cart_id:
            # If cart_id is not found, you might want to handle it
            # For example, redirect or show a message
            return render(request, 'orders/cart_empty.html')  # Assuming you have a cart_empty.html page

        # Retrieve the cart from the database using the cart_id
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            # Handle the case where the cart is not found
            return render(request, 'orders/cart_empty.html')

        # Get all cart items for the specific cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        products_info = ""

        # Loop through the cart items to get the products and quantities
        for item in cart_items:
            product_name = item.product.product_name
            quantity = item.quantity
            variations = ', '.join(
                [variation.variation_value for variation in item.variations.all()])  # Add variations if available
            products_info += f"Product: {product_name}, Quantity: {quantity}, Variations: {variations}\n"

        # Create the message text
        message = f"""
        New Order:
        Name: {first_name} {last_name}
        Phone: {phone}
        Country: {country}
        Region: {region}
        City: {city}
        New Post Branch Number: {new_post_branch}
        Order Note: {order_note}

        Ordered Products:
        {products_info}
        """

        # Telegram bot details
        bot_token = settings.API_BOT

        users = TelegramUser.objects.all()  # Get all users from the database

        # Send the message to each user
        for user in users:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            params = {
                'chat_id': user.chat_id,  # Send the message to each user
                'text': message,
            }

            # Send the request to the Telegram API
            response = requests.get(url, params=params)

        # Redirect to order completion page
        return render(request, 'orders/order_complete.html')
