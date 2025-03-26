from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path("", views.EmployeeView.as_view(), name="employee-list-create"),
    path(
        "<int:employee_id>/",
        views.EmployeeView.as_view(),
        name="employee-detail-update",
    ),
    # path("", views.CustomCBVEmployee.as_view(), name="employee-list-create"),
    # path(
    #     "<int:employee_id>/",
    #     views.CustomCBVEmployee.as_view(),
    #     name="employee-detail",
    # ),
    # path("create/", views.EmployeeCreateView.as_view(), name="create_user"),
    # path("read/<int:pk>/", views.EmployeeDetailView.as_view(), name="read_user"),
    # path("read/all/", views.AllEmployeesListView.as_view(), name="read_all_users"),
    # path(
    #     "update/<pk>",
    #     views.EmployeeUpdateView.as_view(),
    #     name="update_user",
    # ),
    # path(
    #     "delete/<pk>",
    #     views.EmployeeDeleteView.as_view(),
    #     name="delete_user",
    # ),
]

# router = routers.DefaultRouter()
# router.register(r"model-viewset", views.EmployeeViewSet)
# urlpatterns += router.urls
