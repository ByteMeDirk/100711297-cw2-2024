from django.contrib import admin
from django.urls import path, include
from .views import home, user_register, user_login, user_logout, user_edit

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("user_edit/", user_edit, name="user_edit"),
    path("", include("event_management.urls")),
    path("", include("task_management.urls")),
]
