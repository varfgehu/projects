from django.contrib import admin

from .models import Ingredient
from .models import Meal
from .models import Personal
from .models import Measurement
from .models import MealIngredient
from .models import Consumed
from .models import MealItem
from .models import Food, Portion, Intake

# Register your models here.

class MealInline(admin.StackedInline):
    model = Meal.ingredients.through
    extra = 1

class IngredientAdmin(admin.ModelAdmin):
    inlines = [MealInline]

class MealAdmin(admin.ModelAdmin):
    fliter_horizontal = ("ingredients",)


admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(Personal)
admin.site.register(Measurement)
admin.site.register(MealIngredient)
admin.site.register(Consumed)
admin.site.register(MealItem)

admin.site.register(Food)
admin.site.register(Portion)
admin.site.register(Intake)
