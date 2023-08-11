from django.db import models

# Create your models here.

# --Product-----------------------------------------------------------------------------------------------------------#
   
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_image', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    

# --Cart-----------------------------------------------------------------------------------------------------------#

class Cart(models.Model):
    user_session_key = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart ({self.user_session_key})"
    

# --CartItem-----------------------------------------------------------------------------------------------------------#

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    

# --Order-----------------------------------------------------------------------------------------------------------#

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True) 
    address = models.CharField(max_length=200, null=True, blank=True)
    address_two = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    order_note = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order ({self.id})"