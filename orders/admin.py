from django.contrib import admin
from .models import Order, Payment, OrderedProduct
# Register your models here.
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderedProduct)