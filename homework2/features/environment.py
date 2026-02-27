import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_theater_booking.settings")

def before_all(context):
    django.setup()

def before_scenario(context, scenario):
    from django.test.utils import setup_test_environment
    setup_test_environment()

def after_scenario(context, scenario):
    from django.db import connection
    connection.close()