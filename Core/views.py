from django.shortcuts import render, redirect
from Core.models import *
from django.contrib import messages
from decimal import Decimal
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# --home-----------------------------------------------------------------------------------------------------------#

def home(request):
    products = Product.objects.all()
    user_session_key = request.session.session_key
    try:
        # cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(cart_item.quantity for cart_item in Cart.objects.filter(user_session_key=user_session_key, ordered=False))

    except Cart.DoesNotExist:
        cart_quantity_total = 0

    
    context = {
        'cart_quantity_total' : cart_quantity_total,
        'products': products
    }
    return render(request, 'Core/home.html', context)

# --add to cart for home
def add_to_cart_home(request, product_id):
    product = Product.objects.get(id=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    

    cart_item, item_created = Cart.objects.get_or_create(
        user_session_key=session_key,
        product=product,
        ordered=False
    )       


    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"Cart Added Succes fully")
    return redirect('home')


# --product_view-----------------------------------------------------------------------------------------------------------#

def product_view(request, product_id):
    product = Product.objects.get(id=product_id)
     # Assuming you are using user sessions and the session key to identify the cart
    user_session_key = request.session.session_key
    try:
        # cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(cart_item.quantity for cart_item in Cart.objects.filter(user_session_key=user_session_key, ordered=False))

    except Cart.DoesNotExist:
        cart_quantity_total = 0
    

    context = {
        'product': product,
        'cart_quantity_total' : cart_quantity_total
    }
    return render(request, 'Core/product_view.html', context)



# --add_to_cart_product_view------------------------------------------------------------------------------------------------------------#

def add_to_cart_product_view(request, product_id):
    product = Product.objects.get(id=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    

    cart_item, item_created = Cart.objects.get_or_create(
        user_session_key=session_key,
        product=product,
        ordered=False
    )       


    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    

    messages.success(request, f"Cart Added Succes fully")
    return redirect('product_view', product_id=product.id)


# --cart_items_view-----------------------------------------------------------------------------------------------------------#


def cart_items_view(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key, ordered=False).first()

    total_price = Decimal('0.00')
    cart_items = None

    if cart:
        cart_items = Cart.objects.filter(user_session_key=session_key, ordered=False)
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            total_price += item.total_price
        total_price = total_price.quantize(Decimal('0.00'))

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'Core/cart_items.html', context)





# --quantity-----------------------------------------------------------------------------------------------------------#

def increase_quantity(request, item_id):
    item = Cart.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_items_view')

def decrease_quantity(request, item_id):
    item = Cart.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart_items_view')



# --checkout-----------------------------------------------------------------------------------------------------------#

def checkout(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key, ordered=False)
    if request.method == 'POST':
        # Extract the form data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        address_two = request.POST.get('address_two')
        town = request.POST.get('town')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        order_note = request.POST.get('order_note')

        # Create a new order with the provided form data
        order = Order.objects.create(
            
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            address=address,
            address_two=address_two,
            town=town,
            state=state,
            zip=zip_code,
            order_note=order_note,
        )
        order.cart.set(cart)
        
        for field in cart:
            field.ordered = True
            field.save()

        # Calculate total_price and gather cart item details
        total_price = Decimal('0.00')
        cart_details = ""
        for item in cart:
            item_total_price = item.product.price * item.quantity
            total_price += item_total_price
            cart_details += f"\n{item.product.name} - {item.product.price} *x* {item.quantity} *=* {item_total_price}"
        total_price = total_price.quantize(Decimal('0.00'))

        # Construct the WhatsApp URL with order details including cart items
        order_details = f"*Cart Items*:{cart_details}\n*Total*: {total_price}"
        order_details += f"\n\n"
        order_details += f"*Name*: {first_name}, {last_name}\n"
        order_details += f"*Address*: {email}\n"
        order_details += f"*Mobile Number*: {mobile_number}\n"             
        order_details += f"*Address*: {address}\n"
        order_details += f"{address_two}\n"
        order_details += f"*Town*: {town}\n"
        order_details += f"*Status*: {state}\n"
        order_details += f"*Zip Code*: {zip_code}\n"
        order_details += f"*Order Note*: {order_note}\n"
        order_details_encoded = urlencode({'text': order_details})
        whatsapp_url = f"https://api.whatsapp.com/send?phone=+919895291631&{order_details_encoded}"

        # Redirect the user to WhatsApp with the order details pre-filled
        return redirect(whatsapp_url)

    # Calculate total_price and cart_items
    total_price = Decimal('0.00')
    cart_items = None
    if cart:
        cart_items = Cart.objects.filter(user_session_key=session_key, ordered=False)
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            total_price += item.total_price
        total_price = total_price.quantize(Decimal('0.00'))

    context = {
    'cart_items': cart_items,
    'total_price': total_price,
    }
        
    return render(request, 'Core/checkout.html', context)  # Create an empty_cart.html template


# --delete_cart_item-----------------------------------------------------------------------------------------------------------#

def delete_cart_item(request, item_id):
    item = Cart.objects.get(id=item_id)
    item.delete()
    return redirect('cart_items_view')

def delete_all_cart_items(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()
    if cart:
        cart.cart_set.all().delete()
    return redirect('cart_items_view')

# --about------------------------------------------------------------------------------------------------------------#

def about(request):
    user_session_key = request.session.session_key
    try:
        # cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(cart_item.quantity for cart_item in Cart.objects.filter(user_session_key=user_session_key, ordered=False))

    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    context = {
        'cart_quantity_total' : cart_quantity_total,
    }
    return render(request, 'Core/about.html', context)

# --contact-----------------------------------------------------------------------------------------------------------#

def contact(request):
    user_session_key = request.session.session_key
    try:
        # cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(cart_item.quantity for cart_item in Cart.objects.filter(user_session_key=user_session_key, ordered=False))

    except Cart.DoesNotExist:
        cart_quantity_total = 0

    context = {
        'cart_quantity_total' : cart_quantity_total,
    }
    return render(request, 'Core/contact.html', context)

# --shop-----------------------------------------------------------------------------------------------------------#

def shop(request):
    products = Product.objects.all()
    
    # Assuming you are using user sessions and the session key to identify the cart
    user_session_key = request.session.session_key
    try:
        # cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(cart_item.quantity for cart_item in Cart.objects.filter(user_session_key=user_session_key, ordered=False))

    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    context = {
        'products': products,
        'cart_quantity_total': cart_quantity_total
    }
    return render(request, 'Core/shop.html', context)


# --add to cart for shop
def add_to_cart_shop(request, product_id):
    product = Product.objects.get(id=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    

    cart_item, item_created = Cart.objects.get_or_create(
        user_session_key=session_key,
        product=product,
        ordered=False
    )       


    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    

    messages.success(request, f"Cart Added Succes fully")
    return redirect('shop')


# --Order-----------------------------------------------------------------------------------------------------------#

@login_required
def all_orders(request):
    all_orders = Order.objects.all().order_by('-id')
    context = {'all_orders': all_orders}
    return render(request, 'Core/all_orders.html', context)

@login_required
def order_view(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order': order}
    return render(request, 'Core/order_view.html', context)


# --Login-----------------------------------------------------------------------------------------------------------#

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            error = 'Invalid credentials. Please try again.'
    else:
        error = None
    return render(request, 'Core/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('home')