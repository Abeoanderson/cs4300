from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import register_view

app_name = "bookings"

# DRF API router
router = DefaultRouter()
router.register(r"movies",   views.MovieViewSet,   basename="movie-api")
router.register(r"seats",    views.SeatViewSet,    basename="seat-api")
router.register(r"bookings", views.BookingViewSet, basename="booking-api")

urlpatterns = [
    # templates
    path("", views.movie_list,     name="movie_list"),
    path("movies/<int:movie_id>/book/", views.seat_booking,      name="seat_booking"),
    path("my-bookings/", views.booking_history, name="booking_history"),
    path("cancel/<int:booking_id>/", views.cancel_booking,  name="cancel_booking"),
    path("register/", register_view, name="register"),

    # Rest API
    path("api/", include(router.urls)),
]
