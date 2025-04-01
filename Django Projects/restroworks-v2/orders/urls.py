from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("create", views.CreateOrderView.as_view(), name="create_order"),
    path(
        "view/<int:pk>",
        login_required(views.OrderDetailView.as_view()),
        name="retrieve_order",
    ),
    path("view/all", login_required(views.OrderListView.as_view()), name="list_orders"),
    path(
        "view/status/<int:order_id>",
        views.track_order_status,
        name="track_order_status",
    ),
    path(
        "update/<int:order_id>",
        login_required(views.OrderStatusUpdateView.as_view()),
        name="update_order",
    ),
]
