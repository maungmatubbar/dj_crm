from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    # path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("clients/", views.get_clients, name="clients"),
    path("view-client/<int:pk>/", views.view_client, name="view_client"),
    path("delete-client/<int:pk>/", views.delete_client, name="delete_client"),
    path("create-client/", views.create_client, name="create_client"),
    path("update-client/<int:pk>/", views.update_client, name="update_client"),
]
