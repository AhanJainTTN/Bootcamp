from django.db import models
from management.validators.image_validator import validate_image


class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}\n"


class MenuItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    image = models.ImageField(
        upload_to="management/menu_items/",
        validators=[validate_image],
        help_text="Please upload an image with equal height and width.",
        null=True,
    )
    rating = models.FloatField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


STATUS_CHOICES = (
    ("Confirmed", "C"),
    ("In Kitchen", "IK"),
    ("Delivered", "D"),
)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    item_id = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING)
    qty = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
