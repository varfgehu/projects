from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Personal
from django.contrib.auth.models import User
from nutrition.choices import *
from .models import Ingredient, Meal
from datetime import date
from .models import MealItem
from .models import Food, Portion, Intake

# Create your views here.
def home(response):
    #display personal information
    if not response.user.is_authenticated:
        return render(response, "nutrition/login.html", {"message": None})

    try:
        presonal_info = Personal.objects.get(username=response.user)
    except Personal.DoesNotExist:
        return render(response, "nutrition/add_personal_info.html", {})

    context = {
        "personal_info":presonal_info
    }

    return render(response, "nutrition/home.html", context)

def add_personal_info(response):
    if response.method == "POST":
        present_weight = response.POST["present_weight"]
        present_height = response.POST["present_height"]
        sex = response.POST["sex"]
        age = response.POST["age"]
        first_name = User.objects.get(username=response.user)

        personal_info = Personal(username=response.user, first_name=first_name, present_weight=present_weight, present_height=present_height, sex=sex, age=age)
        personal_info.save()

        return HttpResponseRedirect(reverse("home"))

    else:
        return render(response, "nutrition/add_personal_info.html")

def search_meal(response):
    if response.method == "GET":
        context = {
            "types": MEAL_CHOICES,
            "sizes": (FULL_SIZE, SNACK, EXTRA),
            "ingredients": Ingredient.objects.all()
        }
        return render(response, "nutrition/search_meal.html", context)
    else:
        return render(response, "nutrition/search_meal-html")

def add_meal_defined(response, date, meal_type):
    username = response.user
    if response.method == "POST":
        button_pressed = response.POST["add_meal_defined_button"]
        if button_pressed == "Add":
            quantity = response.POST["quantity"]
            ingredient = response.POST["ingredient"]
            print("quantity:" , quantity)
            print("ingredient: ", ingredient)

            food = Food.objects.get(name=ingredient)
            portion = Portion.objects.filter(foods=food, quantity=quantity).first()
            if not portion:
                add_portion = Portion(foods=food, quantity=quantity)
                add_portion.save()
            intake = Intake.objects.filter(user = username, date = date, meal_type = meal_type).first()
            intake.portions.add(portion)

    #         return redirect("add_meal_defined")


    context = {
        "date": date,
        "meal_type": meal_type,
        "foods": Food.objects.all(),
        "intakes": Intake.objects.filter(user = username, date = date, meal_type = meal_type)
    }

    return render(response, "nutrition/add_meal_defined.html", context)




def add_meal(response):
    username = response.user
    today = date.today()
    if response.method == "POST":
        dict = {
            "ingredient1":"quantity1",
            "ingredient2":"quantity2",
            "ingredient3":"quantity3",
            "ingredient4":"quantity4",
            "ingredient5":"quantity5",
            "ingredient6":"quantity6",
            "ingredient7":"quantity7",
            "ingredient8":"quantity8",
            "ingredient9":"quantity9",
            "ingredient10":"quantity10"
        }
        ingredients = ["ingredient1", "ingredient2", "ingredient3", "ingredient4", "ingredient5", "ingredient6", "ingredient7", "ingredient8", "ingredient9", "ingredient10"]
        quantities = ["quantity1", "quantity2", "quantity3", "quantity4", "quantity5", "quantity6", "quantity7", "quantity8", "quantity9", "quantity10"]
        button_pressed = response.POST["add_meal_button"]
        # selected_date = response.POST["date"]
        # meal_type = response.POST["meal_type"]
        # ingredient = response.POST["ingredient"]
        if button_pressed == "Save":
            print("Save button pressed")
            selected_date = response.POST["date"]
            meal_type = response.POST["meal_type"]
            total = {'carb': 0, 'protein': 0, 'fiber': 0, 'calorie': 0}

            add = MealItem.objects.filter(username=username, date=selected_date, meal_type=meal_type)
            if not add:
                add = MealItem(username=username, date=selected_date, meal_type=meal_type,\
                                    ingredient1=response.POST["ingredient1"], quantity1 = 0 if response.POST["quantity1"] == '' else response.POST["quantity1"],\
                                    ingredient2=response.POST["ingredient2"], quantity2 = 0 if response.POST["quantity2"] == '' else response.POST["quantity2"],\
                                    ingredient3=response.POST["ingredient3"], quantity3 = 0 if response.POST["quantity3"] == '' else response.POST["quantity3"],\
                                    ingredient4=response.POST["ingredient4"], quantity4 = 0 if response.POST["quantity4"] == '' else response.POST["quantity4"],\
                                    ingredient5=response.POST["ingredient5"], quantity5 = 0 if response.POST["quantity5"] == '' else response.POST["quantity5"],\
                                    ingredient6=response.POST["ingredient6"], quantity6 = 0 if response.POST["quantity6"] == '' else response.POST["quantity6"],\
                                    ingredient7=response.POST["ingredient7"], quantity7 = 0 if response.POST["quantity7"] == '' else response.POST["quantity7"],\
                                    ingredient8=response.POST["ingredient8"], quantity8 = 0 if response.POST["quantity8"] == '' else response.POST["quantity8"],\
                                    ingredient9=response.POST["ingredient9"], quantity9 = 0 if response.POST["quantity9"] == '' else response.POST["quantity9"],\
                                    ingredient10=response.POST["ingredient10"], quantity10 = 0 if response.POST["quantity10"] == '' else response.POST["quantity10"]
                                    )
                add.save()
            else:
                add.update(ingredient1=response.POST["ingredient1"], quantity1 = 0 if response.POST["quantity1"] == '' else response.POST["quantity1"],\
                ingredient2=response.POST["ingredient2"], quantity2 = 0 if response.POST["quantity2"] == '' else response.POST["quantity2"],\
                ingredient3=response.POST["ingredient3"], quantity3 = 0 if response.POST["quantity3"] == '' else response.POST["quantity3"],\
                ingredient4=response.POST["ingredient4"], quantity4 = 0 if response.POST["quantity4"] == '' else response.POST["quantity4"],\
                ingredient5=response.POST["ingredient5"], quantity5 = 0 if response.POST["quantity5"] == '' else response.POST["quantity5"],\
                ingredient6=response.POST["ingredient6"], quantity6 = 0 if response.POST["quantity6"] == '' else response.POST["quantity6"],\
                ingredient7=response.POST["ingredient7"], quantity7 = 0 if response.POST["quantity7"] == '' else response.POST["quantity7"],\
                ingredient8=response.POST["ingredient8"], quantity8 = 0 if response.POST["quantity8"] == '' else response.POST["quantity8"],\
                ingredient9=response.POST["ingredient9"], quantity9 = 0 if response.POST["quantity9"] == '' else response.POST["quantity9"],\
                ingredient10=response.POST["ingredient10"], quantity10 = 0 if response.POST["quantity10"] == '' else response.POST["quantity10"]\
                )


            print("POST items:")
            for key, value in response.POST.items():
                print(key, value)
                food = Ingredient.objects.filter(name=value).first()
                print("Food: ")
                print(food)
                if food:
                    total["carb"] += food.carb / 100 * quantity
                    total["protein"] += food.protein / 100 * quantity
                    total["fiber"] += food.fiber / 100 * quantity
                    total["calorie"] += food.calorie / 100 * quantity
            print(total)



            items = MealItem.objects.filter(username=username, date=selected_date, meal_type=meal_type)
            context = {
                "date":selected_date,
                "ingredients": Ingredient.objects.all(),
                "items": items[0]
            }

            return render(response, "nutrition/add_meal.html", context)


        elif button_pressed == "Change date/meal":
            print("Change date/meal button pressed")
            button_pressed = response.POST["add_meal_button"]
            selected_date = response.POST["date"]
            meal_type = response.POST["meal_type"]
            items = MealItem.objects.filter(username=username, date=selected_date, meal_type=meal_type)

            if not items:
                pass_item = items
            else:
                pass_item = items[0]

            context = {
                "date":selected_date,
                "ingredients": Ingredient.objects.all(),
                "items": pass_item
            }
            return render(response, "nutrition/add_meal.html", context)

        elif button_pressed == "Add":
            print("Save button pressed")
            for item in response.POST:
                print(item)
            return HttpResponseRedirect(reverse("add_meal"))


    else:
        context = {
            "ingredients": Ingredient.objects.all(),
            "date": today.strftime("%Y-%m-%d"),
            "items": MealItem.objects.filter(username=username, date=today.strftime("%Y-%m-%d"), meal_type="breakfast")
        }
        return render(response, "nutrition/add_meal.html", context)


def create(response):
    return HttpResponse("create")

def values(response):
    return HttpResponse("values")

def login_view(response):
    if response.method == "POST":
        username = response.POST["username"]
        password = response.POST["password"]
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(response, "nutrition/login.html", {"message": "Invalid user data"})
    else:
        return render(response, "nutrition/login.html", {"message": None})

def logout_request(response):
      logout(response)
      return render(response, "nutrition/login.html", {"message": "Logged out."})
