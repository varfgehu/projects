from django.contrib import admin
from .models import Regular_pizza, Sicilian_pizza, Toppings
from .models import OrderCounter
from .models import Order

# Register your models here.
admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Toppings)
admin.site.register(OrderCounter)
admin.site.register(Order)
