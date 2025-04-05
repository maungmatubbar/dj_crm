from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    # path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("clients/", views.get_clients, name="clients"),
    path("export-clients-csv/", views.export_clients_csv, name="export_clients_csv"),
    path("export-clients-pdf/", views.export_clients_pdf, name="export_clients_pdf"),
    path("view-client/<int:pk>/", views.view_client, name="view_client"),
    path("delete-client/<int:pk>/", views.delete_client, name="delete_client"),
    path("create-client/", views.create_client, name="create_client"),
    path("update-client/<int:pk>/", views.update_client, name="update_client"),
    path('client/products/<int:client_pk>/',views.client_products,name="client_products"),
    path("client/create-product/<int:client_pk>/", views.client_create_product, name="client_create_product"),
    path('client/services/<int:client_pk>/',views.client_services,name="client_services"),
    path("client/create-service/<int:client_pk>/", views.client_create_service, name="client_create_service")
]
