from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    # path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("clients/", views.get_clients, name="clients"),
    path("view-client/<int:pk>/", views.view_client, name="view_client"),
]
