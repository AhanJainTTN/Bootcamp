from django.db import models
from menu.validators import validate_image


# class MenuItem(models.Model):
#     item_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     desc = models.CharField(max_length=500)
#     image = models.ImageField(
#         upload_to="management/menu_items/",
#         validators=[validate_image],
#         help_text="Please upload an image with equal height and width.",
#         null=True,
#     )
#     rating = models.FloatField(null=True, blank=True)
#     price = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)


# https://docs.djangoproject.com/en/5.1/ref/models/fields/#datefield
# DateField.auto_now: Automatically set the field to now every time the object is saved. Useful for “last-modified” timestamps.
# DateField.auto_now_add: Automatically set the field to now when the object is first created. Useful for creation of timestamps.
# no need for id since it is automatically generated and managed by Django
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, default="Description")
    image = models.ImageField(
        upload_to="menu/menu_items/",
        validators=[validate_image],
        help_text="Please upload an image with equal height and width.",
        null=True,
        blank=True,
    )
    rating = models.FloatField(default=0.0, blank=True)
    # max_digits: The maximum number of digits allowed in the number. Note that this number must be greater than or equal to decimal_places.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # to track item changes


# FloatField for Ratings since we don’t require exact precision — small floating-point errors don’t matter.
# DecimalField for price since currency must always be accurate and this is the field which will be used for final order value calculations.

# https://docs.djangoproject.com/en/5.1/ref/models/fields/#field-types
# FloatField vs DecimalField
# Floating-point decimal values generally do not have an exact binary representation. This is a side effect of how the CPU represents floating point data. For this reason, you may experience some loss of precision, and some floating-point operations may produce unexpected results - why - Computers store numbers in binary (base-2), but some decimal values cannot be exactly represented in binary, leading to tiny rounding errors. Calculated by FPU so faster since hardware accelerated.
# This is different from Decimal which is stored in Base-10 representaion rather than binary. This is slower since it uses software based integer arithmetic but is exact as compared to Floats.
# We also need to explicitly define the number of decimal places and by default Django uses ROUND_HALF_EVEN as rounding algorithm
# Don't decimals also get converted to binary eventually - yes - however they are stored as scaled integers (ex: 10.1 -> 101) and this scaled integer is converted tp binary for cpu calculations.
# when to use what?
# FloatField: for fast, approximate (still very accurate) calculations like those in machine learning, other scientific applications - cpu accelerated so can be used in games and 3D rendering as well
# DecimalField: Financial applications - money calculations, accounting
