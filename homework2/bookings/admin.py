from django.contrib import admin
from .models import Movie, Seat, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration_display")
    search_fields = ("title",)
    list_filter = ("release_date",)

    @admin.display(description="Duration (mins)", ordering="duration")
    def duration_display(self, obj):
        return obj.duration


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "booking_status")
    list_filter = ("booking_status",)
    search_fields = ("seat_number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "seat", "booking_date")
    list_filter = ("movie", "booking_date")
    search_fields = ("user__username", "movie__title", "seat__seat_number")
    readonly_fields = ("booking_date",)
