from django.db import models
from customers.models import Customer
from menu.models import MenuItem

# Better to use numbers instead of 'C, IK, D' to improve query performance.
STATUS_CHOICES = (
    ("Confirmed", 1),
    ("In Kitchen", 2),
    ("Delivered", 3),
)


# related_name is an attribute that can be used to specify the name of the reverse relation from the related model back to the model that defines the relation - in simple terms if PK of A acts as FK in B and and B defines related name 'abc' for A, A can refer to B, i.e. reverse relation, using related name 'abc'.
# Customer can refer to Order using related_name 'orders'.
class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Confirmed"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        self.total_price = sum(item.total_price() for item in self.items.all())
        self.save()


# Order can refer to OrderItem using related_name 'items'.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_price(self):
        return self.quantity * self.price

    # only update if price is not set otherwise it will update everytime the order is updated
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.menu_item.price
        super().save(*args, **kwargs)


# Flow: Create Order object -> Create all related OrderItem objects (price is updated on save()) -> Update Order.total_price using calculate_total().
