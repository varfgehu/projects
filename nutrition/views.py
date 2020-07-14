from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Personal
from django.contrib.auth.models import User
from nutrition.choices import *
from datetime import date
from .models import Food, Portion, Intake
from .models import Measurement
from .models import Diary
from decimal import Decimal

# Create your views here.
def home(response):
    user = response.user

    if not response.user.is_authenticated:
        return render(response, "nutrition/login.html", {"message": None})

    try:
        presonal_info = Personal.objects.get(username=response.user)
    except Personal.DoesNotExist:
        return render(response, "nutrition/set_personal_info.html", {})

    try:
        Measurement.objects.filter(username=response.user)
    except Measurement.DoesNotExist:
        return render(response, "nutrition/set_personal_info.html", {})

    if response.method == "POST":
        weight = response.POST["weight"]
        bmi = response.POST["bmi"]
        bodyfat = response.POST["bodyFat"]
        bodywater = response.POST["bodyWater"]
        now = date.today().strftime("%Y-%m-%d")

        present_height = float(Personal.objects.filter(username = user).last().present_height)
        age = float(Personal.objects.filter(username = user).last().age)
        activity_level = float(Personal.objects.filter(username = user).last().activity_level)
        calorie_offset = float(Personal.objects.filter(username = user).last().planned_daily_offset)

        measurements = Measurement.objects.filter(username = user, date = now)
        if not measurements:
            measurements = Measurement(username = user, date = now)
            measurements.save()
        Measurement.objects.filter(username = user, date = now).update(weight = weight, bmi = bmi, body_fat = bodyfat, body_water = bodywater)

    latest_weight = float(Measurement.objects.filter(username = user).order_by('-date')[0].weight)
    height = float(Personal.objects.get(username=user).present_height)
    age = float(Personal.objects.get(username=user).age)
    activity_level = float(Personal.objects.get(username=user).activity_level)
    calorie_offset = float(Personal.objects.get(username=user).planned_daily_offset)
    bmr = 66.5 + (13.75 * latest_weight) + (5.003 * height) - (6.755 * age)
    tex = round((bmr * activity_level) + 0.1, 0)
    daily_calorie = tex + calorie_offset
    Personal.objects.filter(username = user).update(needed_calorie = daily_calorie)

    context = {
        "personal_info":presonal_info,
        "latest": Measurement.objects.filter(username = user).order_by('-date')[:1][0],
        "bmr" : bmr,
        "tex": tex,
        "activity_level": activity_level,
        "calorie_offset": calorie_offset,
        "daily_calorie": daily_calorie,
        "weights": Measurement.objects.filter(username = user).order_by('date')
    }

    return render(response, "nutrition/home.html", context)

def set_personal_info(response):
    user = response.user
    if response.method == "POST":
        present_height = float(response.POST["present_height"])
        sex = response.POST["sex"]
        age = float(response.POST["age"])
        first_name = User.objects.get(username = user)
        activity_level = float(response.POST["activity_level"])
        planned_daily_offset = float(response.POST["planned_daily_offset"])
        carb = float(response.POST["carb"])
        protein = float(response.POST["protein"])
        fat = float(response.POST["fat"])

        personal = Personal.objects.filter(username = user)
        if not personal:
            personal = Personal(username = user, first_name = first_name, present_height = present_height, sex = sex, age = age, activity_level = activity_level, planned_daily_offset = planned_daily_offset, needed_carb = carb, needed_protein = protein, needed_fat = fat)
            personal.save()
        Personal.objects.filter(username = user).update(present_height = present_height, sex = sex, age = age, activity_level = activity_level, planned_daily_offset = planned_daily_offset, needed_carb = carb, needed_protein = protein, needed_fat = fat)

        first_measurement = Measurement.objects.filter(username = user).first()
        if not first_measurement:
            first_measurement = Measurement(username = user)
            first_measurement.save()

    context = {
        "personal": Personal.objects.get(username=response.user)
    }

    return render(response, "nutrition/set_personal_info.html", context)

def maintain_food_data(response):
    print("maintain_food_data")
    if response.method == "POST":
        print("POST")
        new_food = response.POST["new_food"]
        new_name = Food.objects.filter(name = new_food)
        if new_name:
            context = {
                "foods": Food.objects.all(),
                "message" :"Food name is already taken, choose another name!"
            }
            return render(response, "nutrition/maintain_food_data.html", context)
        new = Food(name=new_food)
        new.save()
        return food(response, new.id)



    context = {
        "foods": Food.objects.all()
    }

    return render(response, "nutrition/maintain_food_data.html", context)


def food(response, food_id ):
    print("food")
    if response.method == "POST":
        print("POST")
        button_pressed = response.POST["button"]
        if button_pressed == "Modify":
            name = response.POST["name"]
            id = response.POST["id"]
            carb = float(response.POST["carb"])
            fiber = float(response.POST["fiber"])
            sugar = float(response.POST["sugar"])
            protein = float(response.POST["protein"])
            fat = float(response.POST["fat"])
            calorie = float(response.POST["calorie"])

            Food.objects.filter(id=id).update(name=name, carb=carb, fiber=fiber, sugar=sugar, protein=protein, fat=fat, calorie=calorie)
        elif button_pressed == "Delete":
            id = response.POST["id"]
            Food.objects.get(id=id).delete()
            context = {
                "foods": Food.objects.all()
            }

            return render(response, "nutrition/maintain_food_data.html", context)


    context = {
        "food": Food.objects.get(id=food_id)
    }

    return render(response, "nutrition/food.html", context)

def prepare_meal(response):
    today = date.today()
    now = today.strftime("%Y-%m-%d")
    meal_type = "breafast"
    return add_meal_defined(response, now, meal_type)

def add_meal_defined(response, date, meal_type):
    username = response.user
    if response.method == "POST":
        button_pressed = response.POST["add_meal_defined_button"]
        meal_type = response.POST["meal_type"]
        if button_pressed == "Add":
            quantity = response.POST["quantity"]
            ingredient = response.POST["ingredient"]
            print("quantity:" , quantity)
            print("ingredient: ", ingredient)

            food = Food.objects.get(name=ingredient)
            portion = Portion.objects.filter(foods=food, quantity=quantity).first()
            if not portion:
                portion = Portion(foods=food, quantity=quantity)
                portion.save()
            intake = Intake.objects.filter(user = username, date = date, meal_type = meal_type).first()
            if not intake:
                intake = Intake(user = username, date = date, meal_type = meal_type)
                intake.save()
            intake.portions.add(portion)
            diary = Diary.objects.filter(user = username, date = date, meal_type = meal_type).first()
            if not diary:
                diary = Diary(user = username, date = date, meal_type = meal_type)
                diary.save()
            carb = float(diary.carb) + float(quantity) * float(food.carb)
            sugar = float(diary.sugar) + float(quantity) * float(food.sugar)
            protein = float(diary.protein) + float(quantity) * float(food.protein)
            fat = float(diary.fat) + float(quantity) * float(food.fat)
            fiber = float(diary.fiber) + float(quantity) * float(food.fiber)
            calorie = float(diary.calorie) + float(quantity) * float(food.calorie)

            print("*-------------------------------------*")
            print("carb:", str(carb), str(type(carb)))
            print("sugar:", str(sugar), str(type(sugar)))
            print("protein:", str(protein), str(type(protein)))
            print("fat:", str(fat), str(type(fat)))
            print("fiber:", str(fiber), str(type(fiber)))
            print("calorie:", str(calorie), str(type(calorie)))
            print("*-------------------------------------*")




            Diary.objects.filter(user = username, date = date, meal_type = meal_type).update(carb = carb, sugar = sugar, protein = protein, fat = fat, fiber = fiber, calorie = calorie)

        elif button_pressed == "Change date/meal":
            date = response.POST["date"]
            meal_type = response.POST["meal_type"]
        elif button_pressed == "Save":
            # update manytomany field in Intake
            intake = Intake.objects.filter(user = username, date = date, meal_type = meal_type).first()
            intake.portions.clear()
            Diary.objects.filter(user = username, date = date, meal_type = meal_type).update(carb = 0, sugar = 0, protein = 0, fat = 0, fiber = 0, calorie = 0)


            food_in_table = response.POST.getlist('food_in_table')
            quantity_in_table = response.POST.getlist('quantity_in_table')
            length = len(quantity_in_table)
            print(food_in_table)
            print(quantity_in_table)
            print(length)

            for i in range(length):
                print(food_in_table[i])
                print(quantity_in_table[i])

                food = Food.objects.get(name=food_in_table[i])
                portion = Portion.objects.filter(foods=food, quantity=quantity_in_table[i]).first()
                if not portion:
                    portion = Portion(foods=food, quantity=quantity_in_table[i])
                    portion.save()
                intake = Intake.objects.filter(user = username, date = date, meal_type = meal_type).first()
                if not intake:
                    intake = Intake(user = username, date = date, meal_type = meal_type)
                    intake.save()
                intake.portions.add(portion)
                diary = Diary.objects.filter(user = username, date = date, meal_type = meal_type).first()
                if not diary:
                    diary = Diary(user = username, date = date, meal_type = meal_type)
                    diary.save()
                carb = float(diary.carb) + float(quantity_in_table[i]) * float(food.carb)
                sugar = float(diary.sugar) + float(quantity_in_table[i]) * float(food.sugar)
                protein = float(diary.protein) + float(quantity_in_table[i]) * float(food.protein)
                fat = float(diary.fat) + float(quantity_in_table[i]) * float(food.fat)
                fiber = float(diary.fiber) + float(quantity_in_table[i]) * float(food.fiber)
                calorie = float(diary.calorie) + float(quantity_in_table[i]) * float(food.calorie)
                Diary.objects.filter(user = username, date = date, meal_type = meal_type).update(carb = carb, sugar = sugar, protein = protein, fat = fat, fiber = fiber, calorie = calorie)



    if meal_type == "breakfast":
        k = 4.0
    elif meal_type == "lunch":
        k = 4.0
    elif meal_type == "snack1":
        k = 8.0
    elif meal_type == "dinner":
        k = 4.0
    elif meal_type == "snack2":
        k = 8.0
    else:
        k = 4.0

    calorie_needed = Personal.objects.filter(username = username).first().needed_calorie
    needed_carb = Personal.objects.filter(username = username).first().needed_carb
    needed_protein = Personal.objects.filter(username = username).first().needed_protein
    needed_fat = Personal.objects.filter(username = username).first().needed_fat

    calorie_per_carb = 4
    calorie_per_protein = 4
    calorie_per_fat = 9

    print("needed_carb: " + str(needed_carb) + " calorie_needed: " + str(calorie_needed) + " calorie_per_carb: " + str(calorie_per_carb) + " k: " + str(k))

    macros_needed = {
        "carb": round((needed_carb / 100) * (calorie_needed / k) / calorie_per_carb, 2) ,
        "fiber": 35 / k,
        "sugar": 0,
        "protein": round((needed_protein / 100) * (calorie_needed / k) / calorie_per_protein, 2),
        "fat": round((needed_fat / 100) * (calorie_needed / k) / calorie_per_fat, 2),
        "calorie": calorie_needed / k
    }

    context = {
        "date": date,
        "meal_type": meal_type,
        "foods": Food.objects.all(),
        "intakes": Intake.objects.filter(user = username, date = date, meal_type = meal_type),
        "macros_needed" : macros_needed
    }

    return render(response, "nutrition/add_meal_defined.html", context)

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

def register(response):
    if response.method == "POST":
        username = response.POST["username"]
        first_name = response.POST["first_name"]
        password = response.POST["password"]
        password2 = response.POST["password2"]
        email = response.POST["email"]

        new_user = User.objects.filter(username = username)
        if new_user:
            return render(response, "nutrition/register.html", {"message": "Username is already taken. Please choose another one!"})

        if password != password2:
            return render(response, "nutrition/register.html", {"message": "Passwords are not the same!"})

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.save()

        return HttpResponseRedirect(reverse("login"))
    else:
        return render(response, "nutrition/register.html")
