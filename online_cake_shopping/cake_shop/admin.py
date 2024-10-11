from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetails

class AdminProduct(admin.ModelAdmin):
    list_display=['id','name','price','category','description']

class AdminCustomer(admin.ModelAdmin):
    list_display=['id','name','email','password','phno']

class AdminCart(admin.ModelAdmin):
    list_display=['id','phno','product','image','price']


class AdminOrder(admin.ModelAdmin):
    list_display=['id','user','product_name','qty','image','price','order_date','status']


admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Cart,AdminCart)
admin.site.register(OrderDetails,AdminOrder)