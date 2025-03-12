from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("view/all/", views.render_grid, name="render_grid"),
    # path("create/", views.create_item, name="create_item"),
    # path(
    #     "create/", login_required(views.MenuItemFormView.as_view()), name="create_item"
    # ),
    path(
        "create/",
        login_required(views.MenuItemCreateView.as_view()),
        name="create_item",
    ),
    # path("view/<int:item_id>", views.retrieve_item, name="retrieve_item"),
    path(
        "view/<int:pk>/",
        login_required(views.MenuItemDetailView.as_view()),
        name="retrieve_item",
    ),
    # path("view/all", views.list_items, name="list_items"),
    # path(
    #     "view/all/",
    #     views.MenuItemListView.as_view(),
    #     name="list_items",
    # ),
    path("update/<int:item_id>", views.update_item, name="update_item"),
    path("delete/<int:item_id>", views.delete_item, name="delete_item"),
]

app_name = "menu"
