from django.urls import path

from . import views

urlpatterns = [
    path('add_meal_defined/<str:date>/<str:meal_type>', views.add_meal_defined, name="add_meal_defined"),
    path('prepare_meal', views.prepare_meal, name="prepare_meal"),
    path('maintain_food_data', views.maintain_food_data, name="maintain_food_data"),
    path('food/<int:food_id>', views.food, name="food"),
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("log_out", views.logout_request, name="log_out"),
    path("register", views.register, name="register"),
    path("set_personal_info", views.set_personal_info, name="set_personal_info")
]
