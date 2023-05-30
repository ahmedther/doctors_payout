from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("check_task_status/", views.check_task_status, name="check_task_status"),
    path("login/", views.login_page, name="login_page"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),
    path('files/', views.FileListView.as_view(), name='files'),
    path('download/<str:file_name>/', views.download_file, name='download'),
]
