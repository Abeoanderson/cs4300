from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from rest_framework import viewsets, permissions, filters
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


#  Movie view

def movie_list(request):
    """Show all movies, with a search option."""
    query = request.GET.get("q", "").strip()
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(title__icontains=query) # filter movies list

    # Add seat count to each movie
    for movie in movies:
        movie.available_seats = Seat.objects.filter(booking_status="available").count()

    return render(request, "bookings/movie_list.html", {
        "movies": movies,
        "query": query,
    })
# seat booking view

@login_required
def seat_booking(request, movie_id):
    """Display seat map and handle booking form submission."""
    movie = get_object_or_404(Movie, pk=movie_id)
    seats = Seat.objects.all().order_by("seat_number")

    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        seat = get_object_or_404(Seat, pk=seat_id)
        # check if requested seat is available
        if not seat.is_available:
            messages.error(request, f"Seat {seat.seat_number} is no longer available.")
            return redirect("bookings:seat_booking", movie_id=movie.pk)
        # check if another booking for the seat occured
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            messages.error(request, "That seat is already booked for this film.")
            return redirect("bookings:seat_booking", movie_id=movie.pk)
        #book and give confirmation message to user
        Booking.objects.create(movie=movie, seat=seat, user=request.user)
        messages.success(request, f'Booking confirmed! Seat {seat.seat_number} for "{movie.title}".')
        return redirect("bookings:booking_history")

    return render(request, "bookings/seat_booking.html", {
        "movie": movie,
        "seats": seats,
    })
# booking history view

@login_required
def booking_history(request):
    """Show the logged-in user's booking history."""
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("movie", "seat")
        .order_by("-booking_date")
    )

    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    unique_movies = bookings.values("movie").distinct().count()
    recent_count  = bookings.filter(booking_date__gte=month_start).count()

    return render(request, "bookings/booking_history.html", {
        "bookings":      bookings,
        "unique_movies": unique_movies,
        "recent_count":  recent_count,
    })


@login_required
def cancel_booking(request, booking_id):
    """Cancel (delete) a booking and free the seat."""
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if request.method == "POST":
        seat = booking.seat
        booking.delete()
        seat.booking_status = Seat.BookingStatus.AVAILABLE
        seat.save()
        messages.success(request, "Booking cancelled and seat released.")

    return redirect("bookings:booking_history")


#View sets for DRF

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "release_date", "duration"]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["seat_number", "booking_status"]
    ordering_fields = ["seat_number"]


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["movie__title", "seat__seat_number"]
    ordering_fields = ["booking_date"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.select_related("movie", "seat", "user").all()
        return Booking.objects.select_related("movie", "seat", "user").filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)