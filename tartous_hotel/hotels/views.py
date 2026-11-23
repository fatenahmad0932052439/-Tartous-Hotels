from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Min, Q
from .models import Hotel, Room, Booking
from .forms import BookingForm


def get_overlapping_room_ids(check_in, check_out):
    """Return IDs of rooms that have confirmed bookings overlapping [check_in, check_out)."""
    return Booking.objects.filter(
        status='confirmed',
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).values_list('room_id', flat=True)


def parse_search_dates(check_in_str, check_out_str):
    if not check_in_str or not check_out_str:
        return None, None, None
    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        return None, None, "Invalid date format."

    if check_in < date.today():
        return None, None, "Check-in date cannot be in the past."
    if check_out <= check_in:
        return None, None, "Check-out date must be after check-in date."
    return check_in, check_out, None


def home(request):
    """Main page showcasing hotels located in Tartous city."""
    hotels = Hotel.objects.filter(city__iexact='Tartous').annotate(
        min_price=Min('rooms__price_per_night')
    ).order_by('-stars', 'name')

    return render(request, 'hotels/home.html', {'hotels': hotels})


def booking_page(request):
    """Dedicated search and room booking page."""
    city = request.GET.get('city', 'Tartous' if not request.GET else '').strip()
    hotel_id = request.GET.get('hotel', '').strip()
    check_in_str = request.GET.get('check_in', '').strip()
    check_out_str = request.GET.get('check_out', '').strip()
    guests_str = request.GET.get('guests', '2').strip()

    try:
        guests = max(1, int(guests_str))
    except ValueError:
        guests = 2

    check_in, check_out, date_error = parse_search_dates(check_in_str, check_out_str)
    if date_error:
        messages.error(request, date_error)

    rooms = Room.objects.select_related('hotel').filter(capacity__gte=guests)

    if city:
        rooms = rooms.filter(hotel__city__icontains=city)

    if hotel_id.isdigit():
        rooms = rooms.filter(hotel_id=int(hotel_id))

    overlapping_ids = set(get_overlapping_room_ids(check_in, check_out)) if (check_in and check_out) else set()
    if check_in and check_out:
        rooms = rooms.exclude(id__in=overlapping_ids)

    rooms = rooms.order_by('-hotel__stars', 'price_per_night')
    nights = (check_out - check_in).days if (check_in and check_out) else 1

    room_results = []
    for room in rooms:
        room_results.append({
            'room': room,
            'estimated_total': room.price_per_night * nights,
        })

    all_hotels = Hotel.objects.all().order_by('name')
    available_cities = Hotel.objects.values_list('city', flat=True).distinct()

    context = {
        'room_results': room_results,
        'all_hotels': all_hotels,
        'available_cities': available_cities,
        'city': city,
        'selected_hotel': hotel_id,
        'check_in': check_in_str,
        'check_out': check_out_str,
        'guests': guests,
        'nights': nights,
        'has_dates': bool(check_in and check_out),
        'today': date.today().isoformat(),
    }
    return render(request, 'hotels/booking.html', context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    check_in_str = request.GET.get('check_in', '').strip()
    check_out_str = request.GET.get('check_out', '').strip()
    guests_str = request.GET.get('guests', '1').strip()

    try:
        guests = max(1, int(guests_str))
    except ValueError:
        guests = 1

    check_in, check_out, date_error = parse_search_dates(check_in_str, check_out_str)
    if date_error:
        messages.error(request, date_error)

    rooms = hotel.rooms.filter(capacity__gte=guests).order_by('price_per_night')
    overlapping_ids = set(get_overlapping_room_ids(check_in, check_out)) if (check_in and check_out) else set()

    room_list = []
    nights = (check_out - check_in).days if (check_in and check_out) else 1

    for room in rooms:
        room_list.append({
            'room': room,
            'is_available': room.id not in overlapping_ids,
            'estimated_total': room.price_per_night * nights,
        })

    context = {
        'hotel': hotel,
        'room_list': room_list,
        'check_in': check_in_str,
        'check_out': check_out_str,
        'guests': guests,
        'nights': nights,
        'has_dates': bool(check_in and check_out),
        'today': date.today().isoformat(),
    }
    return render(request, 'hotels/hotel_detail.html', context)


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    initial_data = {
        'check_in': request.GET.get('check_in', ''),
        'check_out': request.GET.get('check_out', ''),
        'guests': request.GET.get('guests', 1),
    }

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']

            if guests > room.capacity:
                form.add_error('guests', f"Maximum capacity for this room is {room.capacity} guest(s).")
            else:
                with transaction.atomic():
                    locked_room = Room.objects.select_for_update().get(id=room.id)
                    overlap_exists = Booking.objects.filter(
                        room=locked_room,
                        status='confirmed',
                        check_in__lt=check_out,
                        check_out__gt=check_in,
                    ).exists()

                    if overlap_exists:
                        messages.error(
                            request,
                            "Sorry, this room is already booked for the selected dates. Please try different dates."
                        )
                    else:
                        nights = (check_out - check_in).days
                        booking = form.save(commit=False)
                        booking.room = locked_room
                        booking.total_price = nights * locked_room.price_per_night
                        booking.save()
                        return redirect('booking_success', booking_code=booking.booking_code)
    else:
        form = BookingForm(initial=initial_data)

    return render(request, 'hotels/book_room.html', {
        'room': room,
        'hotel': room.hotel,
        'form': form,
        'today': date.today().isoformat(),
    })


def booking_success(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    return render(request, 'hotels/booking_success.html', {'booking': booking})


def my_bookings(request):
    query = request.GET.get('q', '').strip()
    bookings = []
    if query:
        bookings = Booking.objects.filter(
            Q(booking_code__iexact=query) | Q(guest_email__iexact=query)
        ).select_related('room', 'room__hotel').order_by('-created_at')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings, 'query': query})


def cancel_booking(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    if request.method == 'POST' and booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Booking {booking.booking_code} has been cancelled.")
    return redirect(f"/my-bookings/?q={booking.guest_email}")