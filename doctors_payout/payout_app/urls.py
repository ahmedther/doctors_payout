from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_page, name="login_page"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),
]
