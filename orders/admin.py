from django.contrib import admin
from .models import Regular_pizza, Sicilian_pizza, Toppings
from .models import OrderCounter
from .models import Order
from .models import Sub
from .models import Pasta
from .models import Salad
from .models import Dinner_platter

# Register your models here.
admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Toppings)
admin.site.register(OrderCounter)
admin.site.register(Order)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
