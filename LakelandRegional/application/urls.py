from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api/carts/", views.get_all_carts, name="get_carts"),
    path("api/filter-carts/", views.filter_carts, name="filter_carts"),
]