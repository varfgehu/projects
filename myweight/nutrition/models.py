from django.db import models
from nutrition.choices import *
import datetime

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=64, default="")
    carb = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    sugar = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    protein = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    fat = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    fiber = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    calorie = models.DecimalField(max_digits=7, decimal_places=4, default=0)

    def __str__(self):
        return f"{self.name}"

class Portion(models.Model):
    foods = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="portions")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.foods.name} - {self.quantity} g"

class Intake(models.Model):
    user = models.CharField(max_length=16, default="default")
    date = models.DateField(blank=True, help_text="date of the meal", default=datetime.date.today)
    meal_type = models.CharField(max_length=16, choices = MEAL_CHOICES, default = '1')
    portions = models.ManyToManyField(Portion, blank=True, related_name="intakes")

    def __str__(self):
        return f"{self.user} - {self.date} {self.meal_type}"

class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    carb = models.DecimalField(max_digits=5, decimal_places=2)
    sugar = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    fiber = models.DecimalField(max_digits=5, decimal_places=2)
    calorie = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class Meal(models.Model):
    name = models.CharField(max_length=64)
    meal_type = models.CharField(max_length=16, choices = MEAL_CHOICES, default = '1')
    meal_size = models.CharField(max_length=16, choices = SIZE_CHOICES, default = '1')
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    date = models.DateField(blank=True, help_text="date of the meal", default=datetime.date.today)

    def __str__(self):
        return f"{self.name}"

class MealIngredient(models.Model):
    ingredient = models.ManyToManyField(Ingredient, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity}g - {self.ingredient.name}"

class MealItem(models.Model):
    username = models.CharField(max_length=64)
    date = models.DateField(blank=True, help_text="date of the meal", default=datetime.date.today)
    meal_type = models.CharField(max_length=16, choices = MEAL_CHOICES, default = '1')
    ingredient1 = models.CharField(max_length=64, default="")
    quantity1 = models.IntegerField(default=0)
    ingredient2 = models.CharField(max_length=64, default="")
    quantity2 = models.IntegerField(default=0)
    ingredient3 = models.CharField(max_length=64, default="")
    quantity3 = models.IntegerField(default=0)
    ingredient4 = models.CharField(max_length=64, default="")
    quantity4 = models.IntegerField(default=0)
    ingredient5 = models.CharField(max_length=64, default="")
    quantity5 = models.IntegerField(default=0)
    ingredient6 = models.CharField(max_length=64, default="")
    quantity6 = models.IntegerField(default=0)
    ingredient7 = models.CharField(max_length=64, default="")
    quantity7 = models.IntegerField(default=0)
    ingredient8 = models.CharField(max_length=64, default="")
    quantity8 = models.IntegerField(default=0)
    ingredient9 = models.CharField(max_length=64, default="")
    quantity9 = models.IntegerField(default=0)
    ingredient10 = models.CharField(max_length=64, default="")
    quantity10 = models.IntegerField(default=0)

    total_carb = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    total_protein = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    total_fat = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    total_fiber = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    total_caloria = models.DecimalField(max_digits=5, decimal_places=2, default = 0)

    def __str__(self):
        return f"{self.username} - {self.date} - {self.meal_type}"

class Consumed(models.Model):
    username = models.CharField(max_length=64, default = "default")
    mealingredient = models.ManyToManyField(MealIngredient, blank = True, related_name="mealingredient")
    meal_type = models.CharField(max_length=64, choices = MEAL_CHOICES, default = '1')
    date = models.DateField(blank=True, help_text="date of consume", default=datetime.date.today)

    def __str__(self):
        return f"{self.username} - {self.mealingredient} - {self.meal_type}"

class Personal(models.Model):
    SEX_CHOICES = (
        ('FEMALE', "female"),
        ('MALE', "male")
    )
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    present_height = models.DecimalField(max_digits=4, decimal_places=1)
    sex = models.CharField(max_length=8, choices = SEX_CHOICES, default = '2')
    age = models.IntegerField()
    activity_level = models.DecimalField(max_digits=5, decimal_places = 1, default = 1)
    planned_daily_offset = models.IntegerField(default = 0)

    def __str__(self):
        return f"{self.username}"

class Measurement(models.Model):
    username = models.CharField(max_length = 64)
    date = models.DateField( help_text = "date of consume", default = datetime.date.today)
    weight = models.DecimalField(max_digits = 4, decimal_places = 1, default=99)
    bmi = models.DecimalField(max_digits = 7, decimal_places = 1, default = 99)
    body_fat = models.DecimalField(max_digits = 4, decimal_places = 1, default = 99)
    body_water = models.DecimalField(max_digits = 4, decimal_places = 1, default = 99)


    def __str__(self):
        return f"{self.username} {self.date} weight: {self.weight} kg"
