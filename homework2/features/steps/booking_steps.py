from behave import given, when, then
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking


# Scenario: Book an available seat


@given("there is a movie and an available seat")
def step_db_has_movie_and_seat(context):
    context.client = APIClient()
    context.movie = Movie.objects.create(
        title="Test Movie",
        description="A test",
        release_date="2023-01-01",
        duration=120
    )
    context.seat = Seat.objects.create(
        seat_number="A1",
        booking_status=Seat.BookingStatus.AVAILABLE  
    )

@given("I am a logged-in user")
def step_logged_in_user(context):
    context.user = User.objects.create_user(
        username="testuser",
        password="testuserpass"
    )
    context.client.force_authenticate(user=context.user)

@when("I book the seat for the movie")
def step_book_seat(context):
    context.response = context.client.post(
        "/api/bookings/",
        {
            "movie": context.movie.id,
            "seat": context.seat.id,
            "user": context.user.id
        },
        format="json"
    )

@then("I should receive a 201 status code")
def step_check_201(context):
    assert context.response.status_code == 201, (
        f"Expected 201, got {context.response.status_code}. "
        f"Response: {context.response.data}"
    )

@then("the seat should be marked as booked")
def step_seat_booked(context):
    context.seat.refresh_from_db()
    assert context.seat.booking_status == Seat.BookingStatus.BOOKED, (  # ✅ correct field
        f"Expected seat to be booked, but status={context.seat.booking_status}"
    )


# Scenario: view booking history


@given("I have an existing booking")
def step_existing_booking(context):
    if not hasattr(context, "user"):
        context.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
    if not hasattr(context, "client"):
        context.client = APIClient()
        context.client.force_authenticate(user=context.user)
    if not hasattr(context, "movie"):
        context.movie = Movie.objects.create(
            title="Test Movie",
            description="A test",
            release_date="2023-01-01",
            duration=120
        )
    if not hasattr(context, "seat"):
        context.seat = Seat.objects.create(
            seat_number="A1",
            booking_status=Seat.BookingStatus.AVAILABLE  # ✅ let Booking.save() mark it booked
        )
    context.booking = Booking.objects.create(
        user=context.user,
        movie=context.movie,
        seat=context.seat
    )

@when("I request my booking history")
def step_request_booking_history(context):
    context.response = context.client.get(
        "/api/bookings/",
        format="json"
    )

@then("I should see my past bookings")
def step_see_past_bookings(context):
    assert context.response.status_code == 200, (
        f"Expected 200, got {context.response.status_code}"
    )
    booking_ids = [b["id"] for b in context.response.data]
    assert context.booking.id in booking_ids, (
        f"Booking {context.booking.id} not found in response: {context.response.data}"
    )