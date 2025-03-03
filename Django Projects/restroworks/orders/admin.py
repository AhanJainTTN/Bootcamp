from django.contrib import admin
from orders.models import Order


@admin.action(description="Mark selected orders as Delivered (3)")
def make_delivered(modeladmin, request, queryset):
    queryset.update(status=3)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "status", "total_price", "created_at"]
    actions = [make_delivered]


admin.site.register(Order, OrderAdmin)
