from rest_framework import serializers
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_number", "booking_status", "is_available"]


class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    seat_number = serializers.CharField(source="seat.seat_number", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "movie",
            "movie_title",
            "seat",
            "seat_number",
            "user",
            "username",
            "booking_date",
        ]
        read_only_fields = ["booking_date"]

    def validate(self, data):
        seat = data.get("seat")
        movie = data.get("movie")

        if seat and not seat.is_available:
            raise serializers.ValidationError(
                {"seat": f"Seat {seat.seat_number} is not available."}
            )

        if Booking.objects.filter(movie=movie, seat=seat).exists():
            raise serializers.ValidationError(
                {"seat": "This seat is already booked for the selected movie."}
            )

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)