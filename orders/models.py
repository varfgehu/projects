from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class OrderCounter(models.Model):
    counter = models.IntegerField(default=1)
    user = models.CharField(max_length=32)
    status = models.CharField(max_length=16, default="init")

    def __str__(self):
        return f"User: {self.user} - counter: {self.counter} - status: {self.status}"

class Order(models.Model):
    counter_id = models.IntegerField(default=0)
    item = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.CharField(max_length=32, default="init user")
    status = models.CharField(max_length=16, default="order noted")
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"User: {self.user} - Time: {self.datetime} - counter_id: {self.counter_id}- {self.item} - ${self.price} - Status: {self.status}"


class Regular_pizza(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small} - Lagre: ${self.price_large}"

class Sicilian_pizza(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small} - Lagre: ${self.price_large}"

class Toppings(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small} - Lagre: ${self.price_large}"

class Pasta(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small}"

class Salad(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small}"

class Dinner_platter(models.Model):
    name = models.CharField(max_length=32)
    price_small = models.DecimalField(max_digits=4, decimal_places=2)
    price_large = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - Small: ${self.price_small} - Lagre: ${self.price_large}"
