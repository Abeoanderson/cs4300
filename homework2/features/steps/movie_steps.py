from behave import given, when, then
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bookings.models import Movie
# Scenario: view all movies
# given the database has movies
# when I request the movie Listings
# Then I should recieve a 200 status code
 # and the response I should contian movie titles


@given("the database has movies")
def step_db_has_movies(context):
    Movie.objects.create(
        title="Test Movie",
        description="A test",
        release_date="2023-01-01",
        duration=120
    )
    context.client = APIClient()

@when("I request the movie list")
def step_request_movies(context):
    context.response = context.client.get("/api/movies/")

@then("I should receive a 200 status code")
def step_check_200(context):
    assert context.response.status_code == 200

@then("the response should contain movie titles")
def step_check_titles(context):
    assert len(context.response.data) > 0
    assert "title" in context.response.data[0]
