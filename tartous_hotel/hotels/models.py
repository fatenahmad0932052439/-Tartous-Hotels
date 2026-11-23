from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Tartous')
    address = models.CharField(max_length=255)
    description = models.TextField()
    stars = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    amenities = models.CharField(
        max_length=300,
        default="Sea View, Free Wi-Fi, Swimming Pool, 24h Reception, Free Parking"
    )
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://via.placeholder.com/800x500?text=Tartous+Hotel"

    @property
    def amenities_list(self):
        return [item.strip() for item in self.amenities.split(',') if item.strip()]


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Sea-View Room'),
        ('triple', 'Triple Room'),
        ('suite', 'Luxury Suite'),
        ('chalet', 'Beachfront Chalet'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='double')
    capacity = models.PositiveSmallIntegerField(default=2, help_text="Max guests")
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    has_sea_view = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('hotel', 'room_number')

    def __str__(self):
        return f"{self.hotel.name} | {self.get_room_type_display()} (#{self.room_number})"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return self.hotel.display_image


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_code = models.CharField(max_length=12, unique=True, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=150)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=30)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"TRT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"{self.booking_code} - {self.guest_name}"
# Create your models here.
