from django.urls import path
from . import views


urlpatterns = [
    path("view/grid/", views.render_grid, name="render_grid"),
    path("create/", views.create_item, name="create_item"),
    path("view/<int:item_id>", views.retrieve_item, name="retrieve_item"),
    path("view/all", views.list_items, name="list_items"),
    path("update/<int:item_id>", views.update_item, name="update_item"),
    path("delete/<int:item_id>", views.delete_item, name="delete_item"),
]
