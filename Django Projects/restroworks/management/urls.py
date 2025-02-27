from django.urls import path
from . import views


urlpatterns = [
    path("get", views.get_all_customers, name="get_all_customers"),
    path("add/customer", views.show_customer_form),
]
