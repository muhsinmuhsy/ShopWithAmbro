# --import the path
from django.urls import path

# --import the views 
from Core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('add_to_cart_one/<int:product_id>/', add_to_cart_home, name='add_to_cart_home'),

    path('product_view/<int:product_id>/', product_view, name='product_view'),
    path('add_to_cart_two/<int:product_id>/', add_to_cart_product_view, name='add_to_cart_product_view'),
    
    path('cart_items/', cart_items_view, name='cart_items_view'),
    path('cart_item/increase/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('cart_item/decrease/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('cart_item/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('cart_items/delete_all/', delete_all_cart_items, name='delete_all_cart_items'),

    path('checkout/', checkout, name='checkout'),

    path('about', about, name='about'),

    path('contact', contact, name='contact'),
    
    path('shop', shop, name='shop'),
    path('add_to_cart_three/<int:product_id>/', add_to_cart_shop, name='add_to_cart_shop'),
]