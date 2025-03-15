from django.urls import path
from . import views

# urlpatterns = [
#     path("create/", views.create_user, name="create_user"),
#     path("read/<int:employee_id>", views.read_user, name="read_user"),
#     path("read/all", views.read_all_users, name="read_all_users"),
#     path("update/<int:employee_id>", views.update_user, name="update_user"),
#     path("delete/<int:employee_id>", views.delete_user, name="delete_user"),
# ]

urlpatterns = [
    path("create/", views.EmployeeCreateView.as_view(), name="create_user"),
    path("read/<int:pk>/", views.EmployeeDetailView.as_view(), name="read_user"),
    path("read/all/", views.AllEmployeesListView.as_view(), name="read_all_users"),
    path(
        "update/<pk>",
        views.EmployeeUpdateView.as_view(),
        name="update_user",
    ),
    path(
        "delete/<pk>",
        views.EmployeeDeleteView.as_view(),
        name="delete_user",
    ),
]
