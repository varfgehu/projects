from django.contrib import admin

from .models import Personal
from .models import Measurement
from .models import Food, Portion, Intake, Diary

# Register your models here.

admin.site.register(Personal)
admin.site.register(Measurement)
admin.site.register(Diary)

admin.site.register(Food)
admin.site.register(Portion)
admin.site.register(Intake)
