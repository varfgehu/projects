from django.urls import path

from . import views

urlpatterns = [
    path("search_meal", views.search_meal, name="search_meal"),
    # path("add_meal", views.add_meal, name="add_meal"),
    path('add_meal_defined/<str:date>/<str:meal_type>', views.add_meal_defined, name="add_meal_defined"),
    path("", views.home, name="home"),
    path("create", views.create),
    path("values", views.values),
    path("login", views.login_view, name="login"),
    path("log_out", views.logout_request, name="log_out"),
    path("add_personal_info", views.add_personal_info, name="add_personal_info"),
    path("add_personal_info", views.add_personal_info, name="add_personal_info")
]
