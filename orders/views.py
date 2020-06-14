from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from .models import Regular_pizza, Sicilian_pizza, Toppings
from .models import OrderCounter
from .models import Order

from django.db.models import Max, Sum


# Create your views here.
counter_init = OrderCounter.objects.first()
if counter_init == None:
    new = OrderCounter(counter = 1, user = "init", status="init")
    new.save()

superuser = User.objects.filter(is_superuser=True)
if superuser.count() == 0:
    superuser = User.objects.create_user("master", master@master.com, "mastermaster")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()

def index(response):
    if not response.user.is_authenticated:
        return render(response, "orders/login.html", {"message": None})

    counter_id_for_user = OrderCounter.objects.get(user = response.user)
    print(response.user)
    print(counter_id_for_user.counter)

    total_dict = Order.objects.filter(counter_id = counter_id_for_user.counter).aggregate(Sum('price'))

    context = {
        "regular_pizzas": Regular_pizza.objects.all(),
        "sicilian_pizzas": Sicilian_pizza.objects.all(),
        "toppings": Toppings.objects.all(),
        "user": response.user,
        "items": Order.objects.filter(counter_id = counter_id_for_user.counter),
        "total": total_dict["price__sum"]
    }
    return render(response, "orders/index.html", context)

def add_to_cart(response):
    category = response.POST["category"]
    pizza_name = response.POST["pizza_name"]
    pizza_size = response.POST["pizza_size"]
    price = response.POST["price"]

    print("<------- ADD BUTTON PUSHED ------->\ndetails:")
    print(category)
    print(pizza_name)
    print(pizza_size)
    print(price)

    username = response.user

    order_counter = OrderCounter.objects.get(user = response.user)

    if order_counter.status == "init":
        order_counter.status = "taking orders"
        order_counter.save()


    counter_id_for_the_user = OrderCounter.objects.get(user=response.user).counter
    print(counter_id_for_the_user)

    asseble_item = category.title() + " pizza, " + pizza_name + ", Size: " + pizza_size

    new_item = Order(user=username, counter_id=counter_id_for_the_user, item = asseble_item, price=price)
    new_item.save()
    print("Item added")
    print(new_item)

    if pizza_name == "1 topping":
        number_of_toppings_to_chooes = 1
    elif pizza_name == "2 toppings":
        number_of_toppings_to_chooes = 2
    elif pizza_name == "3 toppings":
        number_of_toppings_to_chooes = 3
    elif pizza_name == "Special":
        number_of_toppings_to_chooes = 4
    else:
        print("unknown pizza name!!")
        number_of_toppings_to_chooes = -1

    counter_id_for_user = OrderCounter.objects.get(user = username)

    total_dict = Order.objects.filter(counter_id = counter_id_for_user.counter).aggregate(Sum('price'))

    if number_of_toppings_to_chooes > 0 :
        context = {
            "toppings": Toppings.objects.all(),
            "topping_allowed": number_of_toppings_to_chooes,
            "user": response.user,
            "items": Order.objects.filter(counter_id = counter_id_for_user.counter),
            "total": total_dict["price__sum"]
        }
        print("render toppings")
        return render(response, "orders/toppings.html", context)
    print("render redirect to index")
    return HttpResponseRedirect("/")


def add_topping(response):
    print(add_topping)
    toppings_left = int(response.POST["number_left"])
    topping_name = response.POST["topping"]
    toppings_left -= 1
    print(toppings_left)
    print(topping_name)

    counter_id_for_the_user = OrderCounter.objects.get(user=response.user).counter

    new_item = Order(user = response.user, counter_id=counter_id_for_the_user, item = topping_name, price=0)
    new_item.save()

    total_dict = Order.objects.filter(counter_id = counter_id_for_the_user).aggregate(Sum('price'))

    context = {
        "toppings": Toppings.objects.all(),
        "topping_allowed": toppings_left,
        "user": response.user,
        "items": Order.objects.filter(counter_id = counter_id_for_the_user),
        "total": total_dict["price__sum"]
    }

    if toppings_left == 0:
        return HttpResponseRedirect("/")
    return render(response, "orders/toppings.html", context)

def cart_buttons(response):
    button_pressed = response.POST["cart_button"]

    if button_pressed == "Checkout":
        counter_id_for_the_user = OrderCounter.objects.get(user=response.user).counter
        orders = Order.objects.filter(user=response.user, status="order taken")
        for order in orders:
            order.status ="checked out"
            order.save()
        order_counter = OrderCounter.objects.get(user=response.user)
        order_counter_max = OrderCounter.objects.aggregate(Max('counter'))
        order_counter.counter = order_counter_max["counter__max"] + 1
        order_counter.save()

        return HttpResponseRedirect("/")
    else:
        counter_id_for_the_user = OrderCounter.objects.get(user=response.user).counter
        Order.objects.filter(counter_id = counter_id_for_the_user).delete()
        return HttpResponseRedirect("/")

def login_view(response):
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)

            try:
                order_counter = OrderCounter.objects.get(user=username)
            except OrderCounter.DoesNotExist:
                order_counter = OrderCounter(counter = 1, user = username, status="init")
                order_counter.save()

            if order_counter.status == "order taken":
                order_counter_max = OrderCounter.objects.aggregate(Max('counter'))
                order_counter.counter = order_counter_max["counter__max"] + 1
                order_counter.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(response, "orders/login.html", {"message": "Invalid user data"})
    else:
        return render(response, "orders/login.html", {"message": None})

def logout_request(response):
      logout(response)
      return render(response, "orders/login.html", {"message": "Logged out."})




def register_page(response):
    if response.method == "POST":
        username = response.POST["username"]
        first_name = response.POST["first_name"]
        last_name = response.POST["last_name"]
        email = response.POST["email"]
        password = response.POST["password"]
        password_conf = response.POST["password_conf"]
        if not password == password_conf:
            return render(response, "orders/register.html", {"message": "Passwords are not the same!"})
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return HttpResponseRedirect(reverse("login"))

    return render(response, "orders/register.html", {})
