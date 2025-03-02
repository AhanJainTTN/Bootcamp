from django.urls import path
from . import views


urlpatterns = [
    # path("get", views.get_all_customers, name="get_all_customers"),
    # path("add/customer", views.add_customer, name="add_customer"),
    path("success-page", views.success_page, name="success_page"),
    # path("add/menu-item", views.add_menu_item, name="add_menu_item"),
]
