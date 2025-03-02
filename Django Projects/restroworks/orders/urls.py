from django.urls import path
from . import views


urlpatterns = [
    path("create", views.create_order, name="create_order"),
    path("view/<int:order_id>", views.retrieve_order, name="retrieve_order"),
    path("view/all", views.list_orders, name="list_orders"),
    path("view/active", views.list_active_orders, name="list_active_orders"),
    path(
        "view/status/<int:order_id>",
        views.track_order_status,
        name="track_order_status",
    ),
    path("update/<int:order_id>", views.update_order, name="update_order"),
    path("cancel/<int:order_id>", views.cancel_order, name="cancel_order"),
    path("delete/<int:order_id>", views.delete_order, name="delete_order"),
]
