from nutrition.access_measurement import *
from nutrition.access_personal import *


def calculate_bmr(weight, height, age):
    return 66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age)

def calculate_tex(bmr, activity_level):
    return round((bmr * activity_level) + 0.1, 0)
