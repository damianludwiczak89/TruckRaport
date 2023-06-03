from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("trucks", views.trucks, name="trucks"),
    path("trucks/<int:truck_id>", views.truck_view, name="truck_view"),
    path("delete_tour/<int:tour_id>", views.delete_tour, name="delete_tour"),
    path("edit_tour", views.edit_tour, name="edit_tour"),
    path("raport", views.raport, name="raport"),
    path("add_spedition", views.add_spedition, name="add_spedition"),
    path("speditions", views.speditions, name="speditions"),
    path("delete_truck/<int:truck_id>", views.delete_truck, name="delete_truck"),
    path("delete_spedition/<int:spedition_id>", views.delete_spedition, name="delete_spedition"),
    path("edit_spedition/<int:spedition_id>", views.edit_spedition, name="edit_spedition"),
    path("raport_file", views.raport_file, name="raport_file"),
    path("guest_login", views.guest_login, name="guest_login"),

    # API routes
    path("default_rate", views.default_rate, name="default_rate"),
    path("get_tour/<int:tour_id>", views.get_tour, name="get_tour"),
    path("edit_truck/<int:truck_id>", views.edit_truck, name="edit_truck"),
]