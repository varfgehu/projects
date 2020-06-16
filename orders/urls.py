from django.urls import path

from . import views

urlpatterns = [
    path("register", views.register_page, name="register"),
    path("login", views.login_view, name="login"),
    path("log_out", views.logout_request, name="logout"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("add_topping", views.add_topping, name="add_topping"),
    path("cart_buttons", views.cart_buttons, name="cart_buttons"),
    path("orders", views.orders, name="orders"),
    path("staff", views.staff, name="staff"),
    path("set_to_done", views.set_to_done, name="set_to_done"),
    path("", views.index, name="index")
]
