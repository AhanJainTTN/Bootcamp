from django.urls import path
from . import views

urlpatterns = [
    path("", views.MetricsView.as_view(), name="metrics"),
    # path("orders/", views.OrderMetricsView.as_view(), name="order_metrics"),
    # path("customers/", views.CustomerMetricsView.as_view(), name="customer_metrics"),
    # path("menu-items/", views.MenuItemMetricsView.as_view(), name="menu_item_metrics"),
]
