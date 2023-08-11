from django.contrib import admin
from Core.models import *
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]

@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CartItem._meta.fields]

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]