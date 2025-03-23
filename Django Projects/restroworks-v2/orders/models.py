from django.db import models
from customers.models import Customer
from menu.models import MenuItem

STATUS_CHOICES = (
    (1, "Confirmed"),
    (2, "In Kitchen"),
    (3, "Delivered"),
    (4, "Cancelled"),
)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        self.total_price = sum(item.total_price() for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity})"
