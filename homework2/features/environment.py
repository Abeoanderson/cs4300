from django.test.utils import setup_test_environment

def before_scenario(context, scenario):
    from django.db import connection
    connection.set_autocommit(False)

def after_scenario(context, scenario):
    from django.db import connection
    connection.rollback()
    connection.set_autocommit(True)