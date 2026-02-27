from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Movie, Seat, Booking
from django.utils import timezone

# test movie model
class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller",
            release_date="2010-07-16",
            duration=148
        )

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.duration, 148)

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Inception")

# test seat model
class SeatModelTest(TestCase):
    def setUp(self):
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False)

    def test_seat_creation(self):
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertFalse(self.seat.is_booked)

# test booking model                                                                                
class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.movie = Movie.objects.create(
            title="Interstellar",
            description="Space exploration",
            release_date="2014-11-07",
            duration=169
        )
        self.seat = Seat.objects.create(seat_number="B2", is_booked=False)
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user,
            booking_date=timezone.now()
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.movie.title, "Interstellar")
        self.assertEqual(self.booking.seat.seat_number, "B2")


# API integration tests

class MovieAPITest(APITestCase):
    def setUp(self):
        Movie.objects.create(
            title="The Matrix",
            description="Reality is a simulation",
            release_date="1999-03-31",
            duration=136
        )

    def test_list_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_movie(self):
        data = {
            "title": "Dune",
            "description": "Desert planet saga",
            "release_date": "2021-10-22",
            "duration": 155
        }
        response = self.client.post("/api/movies/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# test seat api returns valid status
class SeatAPITest(APITestCase):
    def setUp(self):
        Seat.objects.create(seat_number="C3", is_booked=False)

    def test_list_seats(self):
        response = self.client.get("/api/seats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# test booking api returns creation comfirmation and valid status return
class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="booker", password="pass")
        self.client.force_authenticate(user=self.user)
        self.movie = Movie.objects.create(
            title="Avatar",
            description="Blue aliens",
            release_date="2009-12-18",
            duration=162
        )
        self.seat = Seat.objects.create(seat_number="D4", is_booked=False)

    def test_create_booking(self):
        data = {
            "movie": self.movie.id,
            "seat": self.seat.id,
            "booking_date": timezone.now().isoformat()
        }
        response = self.client.post("/api/bookings/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_bookings(self):
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)