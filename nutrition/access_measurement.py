from .models import Measurement

def get_latast_weight(username):
    return Measurement.objects.filter(username = username).order_by('-date')[0]

def get_all_weights(username):
    return Measurement.objects.filter(username = username).order_by('date')

def is_user_measurement_exists(username):
    return Measurement.objects.filter(username = username)

def get_todays_measurement(username, date):
    return Measurement.objects.filter(username = username, date = date)
