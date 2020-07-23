from .models import Personal

def get_height(username):
    return Personal.objects.get(username = username).present_height

def get_age(username):
    return Personal.objects.get(username = username).age

def get_activity_level(username):
    return float(Personal.objects.get(username = username).activity_level)

def get_calorie_offset(username):
    return Personal.objects.get(username = username).planned_daily_offset

def update_needed_calorie(username, daily_calorie):
    Personal.objects.filter(username = username).update(needed_calorie = daily_calorie)

def get_personal_object_by_name(username):
    return Personal.objects.get(username = username)
