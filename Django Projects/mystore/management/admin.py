from django.contrib import admin
from management.models import Salesperson, Order, Customer


class SalespersonAdmin(admin.ModelAdmin):
    list_display = ("salesp_id", "fname", "lname", "yoe")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("cust_id", "first_name", "last_name")


admin.site.register(Salesperson, SalespersonAdmin)
admin.site.register(Order)
admin.site.register(Customer, CustomerAdmin)
