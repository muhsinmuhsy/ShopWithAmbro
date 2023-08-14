from django.shortcuts import render, redirect
from Core.models import *
from django.contrib import messages
from decimal import Decimal
from urllib.parse import quote


# Create your views here.

# --home-----------------------------------------------------------------------------------------------------------#

def home(request):
    products = Product.objects.all()
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
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
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

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
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
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
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Cart Added Succes fully")
    return redirect('product_view', product_id=product.id)


# --cart_items_view-----------------------------------------------------------------------------------------------------------#

def cart_items_view(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()

    # calculation subtotal without tax
    if cart:
        sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        sub_total_price = 0
        cart_items = None

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
        # tax = Decimal('0.05') * total_price  # Calculate 5% tax
        # total_price += tax  # Add tax to the total price
        
        # Format the total_price and tax to have two decimal places
        total_price = total_price.quantize(Decimal('0.00'))
        # tax = tax.quantize(Decimal('0.00'))
    else:
        total_price = Decimal('0.00')
        # tax = Decimal('0.00')
        cart_items = None

        
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        # calculation product one buy one
        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
    else:
        cart_items = []
    

    context = {
        'cart_items': cart_items,
        'total_price' : total_price,
        'sub_total_price' : sub_total_price
    }

    return render(request, 'Core/cart_items.html', context)


# --quantity-----------------------------------------------------------------------------------------------------------#

def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_items_view')

def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart_items_view')



# --checkout-----------------------------------------------------------------------------------------------------------#

def checkout(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
        # tax = Decimal('0.05') * total_price  # Calculate 5% tax
        # total_price += tax  # Add tax to the total price
        
        # Format the total_price and tax to have two decimal places
        total_price = total_price.quantize(Decimal('0.00'))
        # tax = tax.quantize(Decimal('0.00'))
    else:
        total_price = Decimal('0.00')
        # tax = Decimal('0.00')
        cart_items = None

    # calculation subtotal without tax
    if cart:
        sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        sub_total_price = 0
        cart_items = None
    
    if request.method == 'POST':
        # Check if the request method is POST (i.e., form submission after checkout)

        # Get the user's cart using the session key
        session_key = request.session.session_key
        cart = Cart.objects.filter(user_session_key=session_key).first()

        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
            # tax = Decimal('0.05') * total_price  # Calculate 5% tax
            # total_price += tax  # Add tax to the total price
            
            # Format the total_price and tax to have two decimal places
            total_price = total_price.quantize(Decimal('0.00'))
            # tax = tax.quantize(Decimal('0.00'))
        else:
            total_price = Decimal('0.00')
            # tax = Decimal('0.00')
            cart_items = None

        # calculation subtotal without tax
        if cart:
            sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            sub_total_price = 0
            cart_items = None

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
        


        # Create a new order with the provided form data and the cart's total price
        order = Order.objects.create(cart=cart,
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

        # Prepare the order details for WhatsApp message, including cart items
        order_details = "Order Details:\n"
        for cart_item in cart.cartitem_set.all():
            item_total = cart_item.product.price * cart_item.quantity
            order_details += f"*Product:* {cart_item.product.name}, *Price:* {cart_item.product.price}, *Quantity:* {cart_item.quantity}, *Total:* {item_total} \n"

        


        order_details += f"\n----------------------\n"
        order_details += f"\n*Sub Total Price*: {sub_total_price}\n"
        # order_details += f"*Tax*: {'5%'}\n"
        order_details += f"*Total Price*: {total_price}\n"
        order_details += f"----------------------\n"

        

        order_details += f"*Name*: {first_name}, {last_name}\n"
        order_details += f"*Address*: {email}\n"
        order_details += f"*Mobile Number*: {mobile_number}\n"             
        order_details += f"*Address*: {address}\n"
        order_details += f"{address_two}\n"
        order_details += f"*Town*: {town}\n"
        order_details += f"*Status*: {state}\n"
        order_details += f"*Zip Code*: {zip_code}\n"



        
        

        # URL-encode the order_details using urllib.parse.quote
        order_details_encoded = quote(order_details)

        # Construct the WhatsApp URL with order details
        whatsapp_url = f"https://api.whatsapp.com/send?phone=+919614900400&text={order_details_encoded}"

        # Redirect the user to WhatsApp with the order details pre-filled
        return redirect(whatsapp_url)

    else:
        # If the request method is not POST (e.g., initial loading of the checkout page)

        # Get the user's cart using the session key
        session_key = request.session.session_key
        cart = Cart.objects.filter(user_session_key=session_key).first()

        # Retrieve all the cart items associated with the cart
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            # calculation product one buy one
            for item in cart_items:
                item.subtotal = item.product.price * item.quantity
        else:
            cart_items = []

        user_session_key = request.session.session_key
        try:
            cart = Cart.objects.get(user_session_key=user_session_key)
            cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            cart_quantity_total = 0
        
        context = {
            'cart_items': cart_items,
            'total_price' : total_price,
            'sub_total_price' : sub_total_price,
            'cart_quantity_total' : cart_quantity_total, 
        }
        # Render the checkout page with the cart items for display
        return render(request, 'Core/checkout.html', context)



# --delete_cart_item-----------------------------------------------------------------------------------------------------------#

def delete_cart_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart_items_view')

def delete_all_cart_items(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()
    if cart:
        cart.cartitem_set.all().delete()
    return redirect('cart_items_view')

# --about------------------------------------------------------------------------------------------------------------#

def about(request):
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
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
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
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
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
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
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Cart Added Succes fully")
    return redirect('shop')