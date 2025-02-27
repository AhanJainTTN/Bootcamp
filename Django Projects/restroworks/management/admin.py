from django.contrib import admin
from .models import Customer, Order, MenuItem


admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(MenuItem)
