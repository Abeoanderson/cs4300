from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        return self.title


class Seat(models.Model):
    class BookingStatus(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"
        RESERVED = "reserved", "Reserved"

    seat_number = models.CharField(max_length=10, unique=True)
    booking_status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
    )

    class Meta:
        ordering = ["seat_number"]

    def __str__(self):
        return f"Seat {self.seat_number} ({self.get_booking_status_display()})"

    @property
    def is_available(self):
        return self.booking_status == self.BookingStatus.AVAILABLE


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booking_date"]
        unique_together = ("movie", "seat")

    def __str__(self):
        return f"Booking: {self.user.username} → {self.movie.title} (Seat {self.seat.seat_number})"

    def save(self, *args, **kwargs):
        # Mark seat as booked when a booking is created
        self.seat.booking_status = Seat.BookingStatus.BOOKED
        self.seat.save()
        super().save(*args, **kwargs)
