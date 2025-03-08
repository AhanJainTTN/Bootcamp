from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path("signup/", views.user_signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"),
    path("home/", views.render_home, name="render_home"),
    path(
        "bulk-upload/",
        login_required(views.BulkUploadForm.as_view()),
        name="create_from_excel",
    ),
]
