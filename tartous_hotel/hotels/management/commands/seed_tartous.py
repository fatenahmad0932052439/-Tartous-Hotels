from django.core.management.base import BaseCommand
from hotels.models import Hotel, Room


class Command(BaseCommand):
    help = 'Seeds real Tartous hotels and rooms into the database'

    def handle(self, *args, **kwargs):
        hotels_data = [
            {
                'name': 'Grand Hotel Tartous',
                'city': 'Tartous',
                'address': 'East Sea Corniche, Tartous',
                'stars': 5,
                'description': (
                    'The premier 5-star landmark on Tartous East Corniche featuring sea-view rooms and suites, '
                    'the rooftop Grand Sky pool and lounge, SADAF international restaurant, and fitness gym.'
                ),
                'amenities': 'Seafront Corniche, Rooftop Pool, SADAF Restaurant, Gym, Free Wi-Fi, Valet Parking',
                'image_url': 'https://files.cdn-files-a.com/uploads/10841897/2000_6842daad4fa7c.png',
                'rooms': [
                    ('101', 'double', 2, 150.00, True, 'Double Sea-View room with king bed, balcony, and breakfast included.'),
                    ('205', 'triple', 3, 185.00, True, 'Spacious triple room facing the Mediterranean Corniche with pool access.'),
                    ('501', 'suite', 4, 240.00, True, 'Luxury Family Sea-View Suite with lounge area and full amenities.'),
                ],
            },
            {
                'name': 'Royal Inn Hotel',
                'city': 'Tartous',
                'address': 'Sea Corniche, Facing Arwad Island, Tartous',
                'stars': 4,
                'description': (
                    'A 4-star coastal hotel directly on the Tartous Sea Corniche, offering private balconies '
                    'overlooking the Mediterranean Sea and historic Arwad Island with 24-hour electricity and dining.'
                ),
                'amenities': 'Sea-View Balconies, Restaurant, 24h Electricity, Free Wi-Fi, Private Parking',
                'image_url': 'https://royalinntartus.com/assets/img/og-1200x630.jpg',
                'rooms': [
                    ('302', 'double', 2, 90.00, True, 'Sea-view double room with balcony overlooking Arwad Island.'),
                    ('404', 'suite', 4, 145.00, True, 'Royal Sea-View Suite with panoramic coastal balcony and living room.'),
                ],
            },
            {
                'name': 'Shahin Tower Hotel',
                'city': 'Tartous',
                'address': 'Sea Side Road, near Tartous Corniche, Tartous',
                'stars': 4,
                'description': (
                    'A 21-floor 4-star hotel tower facing the sea, offering breathtaking views of the Mediterranean '
                    'and Arwad Island to the west, a panoramic restaurant, summer terrace, and cafe lounge.'
                ),
                'amenities': 'Panoramic Sea View, 21st-Floor Restaurant, Summer Terrace, Free Wi-Fi, Parking',
                'image_url': 'https://syrlista.com/wp-content/uploads/2026/06/shahin-tower-hotel-1.jpg',
                'rooms': [
                    ('701', 'single', 1, 60.00, False, 'Cozy high-floor single room with city skyline view.'),
                    ('1104', 'double', 2, 85.00, True, 'Sea-view double room with balcony overlooking Arwad Island.'),
                    ('1901', 'suite', 4, 160.00, True, 'Executive Tower Suite with panoramic coastline views.'),
                ],
            },
            {
                'name': 'Junada Resort & Hotel',
                'city': 'Tartous',
                'address': 'Maritime Corniche (Antaradus Project), Tartous',
                'stars': 5,
                'description': (
                    'A luxury Mediterranean resort located in the Antaradus waterfront project along the Tartous '
                    'Corniche, featuring outdoor and heated pools, spa facilities, sports tracks, and seaside dining.'
                ),
                'amenities': 'Beachfront Corniche, Outdoor & Heated Pools, Spa & Gym, Restaurants, Free Wi-Fi',
                'image_url': 'https://junada-hotel.com/wp-content/uploads/2025/08/Loz-Outside-Image1-600x540.webp',
                'rooms': [
                    ('112', 'double', 2, 180.00, True, 'Modern luxury double room steps from the Corniche and pools.'),
                    ('224', 'suite', 4, 260.00, True, 'Resort sea-view family suite with full spa and pool access.'),
                ],
            },
            {
                'name': 'Holiday Beach Resort',
                'city': 'Tartous',
                'address': 'Latakia Coastal Highway, Tartous',
                'stars': 5,
                'description': (
                    'Beachfront resort offering 150 suites with sea and mountain views, dedicated adults and kids '
                    'swimming pools, sandy private beach access, outdoor cinema, and landscaped gardens.'
                ),
                'amenities': 'Private Sandy Beach, Kids & Adults Pools, Jacuzzi, Gardens, Free Parking',
                'image_url': 'https://goldenteamsy.com/wp-content/uploads/2024/02/Holiday-Beach-Hotel-1.webp',
                'rooms': [
                    ('B-05', 'chalet', 4, 140.00, True, 'Poolside & beachfront chalet ideal for families up to 4 guests.'),
                    ('V-01', 'suite', 5, 210.00, True, 'Large Sea & Mountain View Suite with private terrace.'),
                ],
            },
            {
                'name': 'Blue Beach Hotel',
                'city': 'Tartous',
                'address': 'Corniche Al-Bahri, Tartous',
                'stars': 3,
                'description': (
                    'A comfortable 3-star seafront hotel on Corniche Al-Bahri offering great value for money, '
                    '24/7 front desk service, dining room with wide sea windows, and easy access to downtown Tartous.'
                ),
                'amenities': 'Corniche Location, Dining Room, 24/7 Reception, Free Wi-Fi',
                'image_url': 'https://cfooumftuesvlmphgyhb.supabase.co/storage/v1/object/public/compressed_images/0.6110938813675867.PNG',
                'rooms': [
                    ('104', 'single', 1, 45.00, False, 'Budget-friendly single room near the Corniche.'),
                    ('208', 'double', 2, 65.00, True, 'Sea-view double room with bright windows and breakfast.'),
                ],
            },
        ]

        for h_data in hotels_data:
            hotel, _ = Hotel.objects.update_or_create(
                name=h_data['name'],
                defaults={
                    'city': h_data['city'],
                    'address': h_data['address'],
                    'stars': h_data['stars'],
                    'description': h_data['description'],
                    'amenities': h_data['amenities'],
                    'image': None,
                    'image_url': h_data['image_url'],
                }
            )
            for r_num, r_type, cap, price, sea_view, desc in h_data['rooms']:
                Room.objects.update_or_create(
                    hotel=hotel,
                    room_number=r_num,
                    defaults={
                        'room_type': r_type,
                        'capacity': cap,
                        'price_per_night': price,
                        'has_sea_view': sea_view,
                        'description': desc,
                    }
                )
        self.stdout.write(self.style.SUCCESS('Tartous hotels and rooms loaded successfully!'))