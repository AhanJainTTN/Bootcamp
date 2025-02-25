from django.urls import path
from . import views


urlpatterns = [
    path("get", views.get_all_customers, name="get_all_customers"),
    path("get/<str:name>", views.get_customer, name="get_customer"),
    path("me", views.who_am_i, name="who_am_i"),
]
