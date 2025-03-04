from django.urls import path
from . import views


urlpatterns = [
    path("view/<int:customer_id>", views.retrieve_customer, name="retrieve_customer"),
    path("view/all", views.list_customers, name="list_customers"),
    path("update/<int:customer_id>", views.update_customer, name="update_customer"),
    path("delete/<int:customer_id>", views.delete_customer, name="delete_customer"),
]
