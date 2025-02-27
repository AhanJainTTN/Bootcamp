from django.db import models


class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        managed = False
        db_table = "customers"


class Salesperson(models.Model):
    salesp_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    yoe = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.fname} {self.lname}"

    class Meta:
        managed = False
        db_table = "salespersons"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Customer, models.DO_NOTHING)
    salesp = models.ForeignKey(Salesperson, models.DO_NOTHING, blank=True, null=True)
    qty = models.PositiveSmallIntegerField()
    date = models.DateField()

    class Meta:
        managed = False
        db_table = "orders"
