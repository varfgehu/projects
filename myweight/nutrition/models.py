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

class Diary(models.Model):
    user = models.CharField(max_length=16, default="default")
    date = models.DateField(blank=True, help_text="date of the meal", default=datetime.date.today)
    meal_type = models.CharField(max_length=16, choices = MEAL_CHOICES, default = '1')
    carb = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    calorie = models.DecimalField(max_digits=5, decimal_places=2, default = 0)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.meal_type}"

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
    needed_calorie = models.IntegerField( default = 2000)
    needed_carb = models.IntegerField( default = 40)
    needed_protein = models.IntegerField( default = 30)
    needed_fat = models.IntegerField( default = 30)

    def __str__(self):
        return f"{self.username}"

class Measurement(models.Model):
    username = models.CharField(max_length = 64)
    date = models.DateField( help_text = "date of consume", default = datetime.date.today)
    weight = models.DecimalField(max_digits = 4, decimal_places = 1, default=0)
    bmi = models.DecimalField(max_digits = 7, decimal_places = 1, default = 0)
    body_fat = models.DecimalField(max_digits = 4, decimal_places = 1, default = 0)
    body_water = models.DecimalField(max_digits = 4, decimal_places = 1, default = 0)


    def __str__(self):
        return f"{self.username} {self.date} weight: {self.weight} kg"
