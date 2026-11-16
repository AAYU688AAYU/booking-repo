from datetime import date, timedelta, time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import (
    Destination, TourPackage, Hotel, RoomType,
    SeasonalPricing, GuideProfile, TourSlot
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds sample hotels, room types, seasonal rules, and guide profiles'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Phase 2: Hotels, Room Types, Seasonal Pricing & Guides...")

        # 1. Ensure a vendor user exists
        vendor_user, _ = User.objects.get_or_create(
            email='vendor@voyagecraft.com',
            defaults={
                'full_name': 'Grand Heritage Resorts Ltd',
                'role': 'VENDOR',
                'phone_number': '+91 98765 43210',
                'is_verified': True,
            }
        )

        # 2. Seed Hotels
        hotels_data = [
            {
                'dest_name': 'Shimla',
                'name': 'Wildflower Hall & Spa, An Oberoi Resort',
                'slug': 'wildflower-hall-oberoi-shimla',
                'address': 'Chharabra, Shimla, Himachal Pradesh 171012',
                'star_rating': 5,
                'description': 'Perched at 8,250 feet amidst 22 acres of virgin cedar forests. Features an open-air heated whirlpool overlooking snow peaks and colonial Victorian architecture.',
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80',
                'amenities': ['Heated Infinity Whirlpool', 'Oberoi Spa & Ayurvedic Therapies', 'Pine Forest Trails', 'Fine Dining The Restaurant', 'High-Speed Starlink WiFi'],
                'rooms': [
                    {'name': 'Deluxe Garden View Room', 'slug': 'deluxe-garden-view', 'price': '320.00', 'capacity': 2, 'beds': '1 King Bed', 'size': 42},
                    {'name': 'Premier Mountain View Room', 'slug': 'premier-mountain-view', 'price': '480.00', 'capacity': 2, 'beds': '1 King Bed', 'size': 50},
                    {'name': 'Lord Kitchener Heritage Suite', 'slug': 'lord-kitchener-suite', 'price': '950.00', 'capacity': 3, 'beds': '1 King Bed + 1 Daybed', 'size': 95},
                ]
            },
            {
                'dest_name': 'Manali',
                'name': 'The Himalayan Castle Resort & Spa',
                'slug': 'the-himalayan-castle-resort-manali',
                'address': 'Hadimba Road, Manali, Himachal Pradesh 175131',
                'star_rating': 5,
                'description': 'Victorian Gothic castle architecture set amidst cherry and apple orchards. Boasts antique cast-iron fireplaces, medieval dining halls, and Pir Panjal panorama.',
                'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80',
                'amenities': ['Apple Orchard Veranda', 'Fireplace Parlour', 'Dungeon Bar & Lounge', 'Heated Swimming Pool', 'Himalayan Trek Concierge'],
                'rooms': [
                    {'name': 'Castle Chamber Premier', 'slug': 'castle-chamber-premier', 'price': '180.00', 'capacity': 2, 'beds': '1 Queen Bed', 'size': 38},
                    {'name': 'Grand Tower Suite with Fireplace', 'slug': 'grand-tower-suite', 'price': '340.00', 'capacity': 3, 'beds': '1 King Bed + Fireplace Alcove', 'size': 65},
                ]
            },
            {
                'dest_name': 'Amalfi Coast',
                'name': 'Belmond Hotel Caruso & Cliffside Haven',
                'slug': 'belmond-hotel-caruso-amalfi',
                'address': 'Piazza San Giovanni del Toro, 2, 84010 Ravello SA, Italy',
                'star_rating': 5,
                'description': 'An 11th-century palace set on a cliff 1,000 feet above the Mediterranean. Famed for its cliff-edge elliptical infinity pool and rose-arbor pergolas.',
                'image_url': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80',
                'amenities': ['Suspended Infinity Pool', 'Private Riva Yacht Excursions', 'Michelin-starred Belvedere Restaurant', 'Lemongrove Wellness Garden'],
                'rooms': [
                    {'name': 'Sea View Deluxe Room', 'slug': 'sea-view-deluxe', 'price': '750.00', 'capacity': 2, 'beds': '1 King Bed', 'size': 45},
                    {'name': 'Exclusive Belmond Signature Suite', 'slug': 'exclusive-belmond-suite', 'price': '1850.00', 'capacity': 3, 'beds': '1 Super King Bed + Terrace', 'size': 110},
                ]
            },
            {
                'dest_name': 'Kyoto & Fuji',
                'name': 'Hoshinoya Kyoto River Pavilion Ryokan',
                'slug': 'hoshinoya-kyoto-ryokan',
                'address': '11-2 Arashiyama Genrokuzancho, Nishikyo Ward, Kyoto',
                'star_rating': 5,
                'description': 'A century-old riverside ryokan accessible only by a traditional wooden riverboat gliding past Arashiyama’s red maple canyons. Features tatami salons and kaiseki masters.',
                'image_url': 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80',
                'amenities': ['Scenic Riverboat Transit', 'Private Kaiseki Dining Pavilion', 'Zen Meditation Terrace', 'Hinoki Cedar Baths', 'Tea Ceremony Masterclasses'],
                'rooms': [
                    {'name': 'Mizunone River View Pavilion', 'slug': 'mizunone-river-pavilion', 'price': '620.00', 'capacity': 2, 'beds': 'Traditional Futon on Cedar Tatami', 'size': 55},
                    {'name': 'Tsukihashi Maple Panoramic Suite', 'slug': 'tsukihashi-maple-suite', 'price': '1100.00', 'capacity': 3, 'beds': 'Luxury Futon Suite + Private Garden', 'size': 85},
                ]
            }
        ]

        for h_data in hotels_data:
            dest = Destination.objects.filter(name__icontains=h_data['dest_name']).first()
            if not dest:
                continue

            hotel, _ = Hotel.objects.get_or_create(
                slug=h_data['slug'],
                defaults={
                    'destination': dest,
                    'owner': vendor_user,
                    'name': h_data['name'],
                    'address': h_data['address'],
                    'star_rating': h_data['star_rating'],
                    'description': h_data['description'],
                    'image_url': h_data['image_url'],
                    'amenities': h_data['amenities'],
                    'is_featured': True,
                }
            )

            for r_data in h_data['rooms']:
                room, _ = RoomType.objects.get_or_create(
                    hotel=hotel,
                    slug=r_data['slug'],
                    defaults={
                        'name': r_data['name'],
                        'max_occupancy': r_data['capacity'],
                        'base_price_per_night': Decimal(r_data['price']),
                        'total_rooms': 8,
                        'bed_type': r_data['beds'],
                        'room_size_sqm': r_data['size'],
                        'image_url': h_data['image_url'],
                        'amenities': ['Smart Climate Control', 'L\'Occitane Bath Amenities', 'Nespresso Bar', 'Evening Turn-Down Service']
                    }
                )

                # Add a seasonal peak pricing rule (1.3x surge)
                today = date.today()
                SeasonalPricing.objects.get_or_create(
                    room_type=room,
                    name='Holiday Season Surge',
                    defaults={
                        'start_date': today + timedelta(days=20),
                        'end_date': today + timedelta(days=35),
                        'price_multiplier': Decimal('1.30'),
                    }
                )

        # 3. Seed Guide Profiles and Tour Slots
        guides_data = [
            {
                'email': 'tsering.himalaya@voyagecraft.com',
                'name': 'Tsering Norbu Sherpa',
                'bio': 'High-altitude mountaineer with 12 summits across Himachal & Ladakh. Wilderness First Responder certified.',
                'languages': ['English', 'Hindi', 'Tibetan'],
                'experience': 11,
                'rating': 4.98,
                'dest_name': 'Manali'
            },
            {
                'email': 'marco.ravello@voyagecraft.com',
                'name': 'Marco Esposito',
                'bio': '3rd-generation Amalfi skipper, sommelier, and marine conservation advocate with deep maritime knowledge.',
                'languages': ['English', 'Italian', 'Spanish'],
                'experience': 14,
                'rating': 5.0,
                'dest_name': 'Amalfi Coast'
            },
            {
                'email': 'kenji.kyoto@voyagecraft.com',
                'name': 'Kenji Takahashi',
                'bio': 'Kyoto cultural ambassador, licensed tea ceremony practitioner, and traditional Japanese architecture scholar.',
                'languages': ['English', 'Japanese'],
                'experience': 9,
                'rating': 4.96,
                'dest_name': 'Kyoto & Fuji'
            }
        ]

        for g_data in guides_data:
            g_user, _ = User.objects.get_or_create(
                email=g_data['email'],
                defaults={
                    'full_name': g_data['name'],
                    'role': 'GUIDE',
                    'is_verified': True,
                }
            )

            profile, _ = GuideProfile.objects.get_or_create(
                user=g_user,
                defaults={
                    'bio': g_data['bio'],
                    'license_number': f"LIC-TRV-{g_data['experience']}88",
                    'spoken_languages': g_data['languages'],
                    'experience_years': g_data['experience'],
                    'rating': g_data['rating'],
                    'is_verified': True,
                }
            )

            dest = Destination.objects.filter(name__icontains=g_data['dest_name']).first()
            if dest:
                profile.destinations.add(dest)
                # Attach slots to tours in that destination
                tour = TourPackage.objects.filter(destination=dest).first()
                if tour:
                    for i in range(1, 8):
                        slot_d = date.today() + timedelta(days=i * 2)
                        TourSlot.objects.get_or_create(
                            tour=tour,
                            guide=profile,
                            slot_date=slot_d,
                            start_time=time(9, 0),
                            defaults={
                                'end_time': time(13, 0),
                                'max_capacity': tour.group_size_max,
                                'booked_count': 2,
                                'is_active': True,
                            }
                        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Phase 2 data!"))
