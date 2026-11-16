from django.core.management.base import BaseCommand
from api.models import Destination, TourPackage, Booking, Review


class Command(BaseCommand):
    help = 'Seeds initial destinations, tours, reviews, and sample bookings'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding with Indian destinations and budget/luxury tours...")

        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        TourPackage.objects.all().delete()
        Destination.objects.all().delete()

        # ---------------------------------------------------------------------
        # 1. DESTINATIONS
        # ---------------------------------------------------------------------
        # Indian Destinations
        dest_shimla = Destination.objects.create(
            name="Shimla",
            country="India",
            region="India & Asia",
            description="The Queen of Hills nestled in pine-scented Himalayan ridges. Famous for historic Mall Road, neo-Gothic Christ Church, panoramic Jakhoo peak, and heritage Kalka toy trains.",
            image_url="https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80",
            climate="Cool Alpine (12°C - 22°C Summer / -2°C - 8°C Winter Snow)",
            best_season="March - June (Summer) & Dec - Feb (Winter Snow)",
            is_featured=True
        )

        dest_manali = Destination.objects.create(
            name="Manali",
            country="India",
            region="India & Asia",
            description="High-altitude Himalayan playground with snow-capped Pir Panjal peaks, rushing Beas River, Solang Valley adventures, Old Manali cafes, and Atal Tunnel gateway to Lahaul.",
            image_url="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
            climate="Sub-Alpine (10°C - 24°C Summer / -5°C - 4°C Snow Season)",
            best_season="April - June & Oct - Nov / Dec - Feb for Snow",
            is_featured=True
        )

        dest_meghalaya = Destination.objects.create(
            name="Meghalaya",
            country="India",
            region="India & Asia",
            description="The Abode of Clouds: bio-engineered double-decker living root bridges, the crystal-transparent waters of Dawki river, roaring Nohkalikai Falls, and serene Khasi hill villages.",
            image_url="https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1200&q=80",
            climate="Misty & Refreshing (14°C - 24°C)",
            best_season="October - April",
            is_featured=True
        )

        # International Destinations
        dest_amalfi = Destination.objects.create(
            name="Amalfi Coast",
            country="Italy",
            region="Europe",
            description="Dramatic Mediterranean cliffs, pastel-hued villages cascading into sapphire waters, scented lemon groves, and timeless Italian elegance.",
            image_url="https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80",
            climate="Mediterranean Sunny (24°C - 30°C)",
            best_season="May - October",
            is_featured=True
        )

        dest_kyoto = Destination.objects.create(
            name="Kyoto & Fuji",
            country="Japan",
            region="Asia",
            description="Centuries-old Zen temples, secluded bamboo groves, geisha quarters, Mount Fuji reflections, and Michelin-starred culinary artistry.",
            image_url="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
            climate="Temperate (18°C - 25°C)",
            best_season="March - May & Oct - Nov",
            is_featured=True
        )

        dest_swiss = Destination.objects.create(
            name="Swiss Alps",
            country="Switzerland",
            region="Europe",
            description="Snow-crowned summits, crystal-clear turquoise alpine lakes, legendary cogwheel railways, and idyllic chalet hamlets.",
            image_url="https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80",
            climate="Alpine Fresh (12°C - 22°C)",
            best_season="June - September & Dec - March",
            is_featured=True
        )

        dest_bali = Destination.objects.create(
            name="Bali & Nusa",
            country="Indonesia",
            region="Asia",
            description="Emerald terraced rice fields, sacred cliffside water temples, coral reef lagoons, and world-renowned holistic wellness retreats.",
            image_url="https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
            climate="Tropical Warm (28°C - 32°C)",
            best_season="April - October",
            is_featured=False
        )

        dest_serengeti = Destination.objects.create(
            name="Serengeti & Ngorongoro",
            country="Tanzania",
            region="Africa",
            description="The greatest wildlife spectacle on Earth: roaming lions, majestic elephant herds, and endless golden savannah sunsets.",
            image_url="https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80",
            climate="Savannah Mild (22°C - 28°C)",
            best_season="July - October & Jan - Feb",
            is_featured=False
        )

        # ---------------------------------------------------------------------
        # 2. TOUR PACKAGES (Student Budget vs. Ultra Luxury)
        # ---------------------------------------------------------------------

        # --- SHIMLA: Student Budget (₹2,000 / $24) ---
        tour_shimla_student = TourPackage.objects.create(
            destination=dest_shimla,
            title="Shimla Student Backpacker & Heritage Trail (Under 2K)",
            slug="shimla-student-backpacker-trail",
            category="Student",
            duration_days=2,
            travel_time="Approx. 3.5 hrs from Chandigarh / 7 hrs HRTC Volvo from Delhi / Scenic Toy Train from Kalka (5 hrs)",
            price_per_person=23.67,  # Exact ₹2,000 INR @ 84.5 rate
            original_price=35.50,   # ~₹3,000
            group_size_max=16,
            difficulty="Easy",
            rating=4.88,
            review_count=94,
            short_description="Explore Shimla on an unbeatable ₹2,000 student budget! Backpacker hostel stay near Mall Road, Jakhoo temple hike, sunset at The Ridge, and local siddu food trail.",
            detailed_overview="Crafted especially for college students, solo backpackers, and budget weekenders. Experience Shimla's colonial charms without breaking the bank. Stay in a clean, vibrant youth hostel with a rooftop view of the mountains, hike to the highest peak at Jakhoo Temple, stroll through The Ridge and Lakkar Bazaar, and ride the historic Kalka-Shimla Toy Train.",
            image_url="https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "Pocket-friendly ₹2,000 budget package with certified youth hostel dormitory stay",
                "Sunset panorama from Scandal Point and iconic Christ Church at The Ridge",
                "Pine forest hike to Jakhoo Temple (highest point in Shimla at 2,455m)",
                "Local street food tasting coupon: hot Himachali siddu & masala chai",
                "Student ID discount assistance for Viceregal Lodge and Toy Train tickets"
            ],
            included=[
                "1 night bunk bed stay at verified Backpacker Youth Hostel near Mall Road",
                "Hot morning breakfast with tea/coffee",
                "Local student trail leader for walking tours & photo spots",
                "Jakhoo temple nature hike coordination",
                "Luggage drop service before check-in and after checkout"
            ],
            excluded=[
                "Bus/train fares to/from Shimla (HRTC bus tickets ~₹450 from Delhi)",
                "Personal shopping at Lakkar Bazaar",
                "Ropeway tickets to Jakhoo (approx. ₹250 optional)"
            ],
            itinerary=[
                {"day": 1, "title": "Arrive in Shimla, Check-in & The Ridge Sunset", "description": "Arrive at Old Bus Stand or Shimla Railway Station via Toy Train. Short walk/lift to your youth hostel. Unpack and head to Mall Road. Visit Christ Church, enjoy the sunset over Shivalik ranges at Scandal Point. Evening rooftop acoustic campfire and game night with fellow student backpackers."},
                {"day": 2, "title": "Jakhoo Hill Nature Trek & Lakkar Bazaar Departure", "description": "Morning scenic hike through whispering deodar trees up to Jakhoo Temple. Watch the playful monkeys and take panoramic photos of snowy peaks. Descend into Lakkar Bazaar for local Himachali siddu lunch. Stroll down lower bazaar for souvenirs and catch your evening bus or toy train back."}
            ],
            upcoming_dates=["2026-05-02", "2026-05-16", "2026-06-06", "2026-06-20", "2026-07-04"],
            is_featured=True,
            is_trending=True
        )

        # --- SHIMLA: Luxury Grandeur ($480 / ₹40,500) ---
        tour_shimla_luxury = TourPackage.objects.create(
            destination=dest_shimla,
            title="Shimla British Colonial Grandeur & Oberoi Forest Sanctuary",
            slug="shimla-british-colonial-grandeur",
            category="Luxury",
            duration_days=4,
            travel_time="Chauffeured Mercedes from Chandigarh Airport (3 hrs) or Chartered Heli-taxi to Shimla Airport (20 mins)",
            price_per_person=480.00,
            original_price=580.00,
            group_size_max=8,
            difficulty="Easy",
            rating=4.97,
            review_count=42,
            short_description="Relive the opulent Raj era with 5-star colonial heritage stays, private cedar forest spa sessions, high tea at Viceregal Lodge, and chauffeured sightseeing.",
            detailed_overview="An aristocratic retreat into the colonial summer capital of the British Empire. Stay in luxury heritage suites overlooking virgin cedar and pine forests, indulge in bespoke Ayurvedic spa treatments, and enjoy exclusive private access to historic estates with a master colonial historian.",
            image_url="https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "3 nights in 5-star Heritage Cedar Suite with private fireplace",
                "Private vintage high tea at the historic Viceregal Lodge lawns",
                "Ayurvedic forest wellness spa therapy with mountain views",
                "Chauffeured luxury SUV for all excursions including Mashobra & Kufri"
            ],
            included=[
                "3 nights luxury accommodation",
                "All gourmet breakfasts and 3 multi-course fine dining dinners",
                "Private Mercedes SUV chauffeur with airport pickup/drop",
                "Personal heritage guide"
            ],
            excluded=[
                "Airfare to Chandigarh / Shimla",
                "Personal spa add-ons and premium liquor"
            ],
            itinerary=[
                {"day": 1, "title": "VIP Chauffeur Pickup & Colonial Welcome", "description": "Meet private chauffeur at Chandigarh airport. Scenic drive up the Himalayan expressway to your heritage resort. Welcome Himachali apple wine and fireplace dinner."},
                {"day": 2, "title": "Private Colonial Heritage & Viceregal Lodge", "description": "Exclusive guided tour through the corridors of the historic Viceregal Lodge where the partition treaties were discussed. High tea on the garden lawns."},
                {"day": 3, "title": "Mashobra Cedar Walks & Forest Spa", "description": "Morning nature walk through protected Mashobra pine woods. Afternoon signature cedar oil deep-tissue spa massage."},
                {"day": 4, "title": "Breakfast with Mountain Panorama & Departure", "description": "Champagne breakfast on the terrace overlooking the Himalayas. Private transfer back to Chandigarh airport."}
            ],
            upcoming_dates=["2026-05-10", "2026-06-05", "2026-07-15", "2026-09-12"],
            is_featured=False,
            is_trending=False
        )

        # --- MANALI: Student Adventure (₹3,200 / $38) ---
        tour_manali_student = TourPackage.objects.create(
            destination=dest_manali,
            title="Manali Student Riverside Camp, Jogini Falls & Solang Snow Adventure",
            slug="manali-student-riverside-adventure",
            category="Student",
            duration_days=3,
            travel_time="Overnight AC Volvo bus from Delhi (11-12 hrs) or Chandigarh (7-8 hrs)",
            price_per_person=37.87,  # Exact ₹3,200 INR @ 84.5 rate
            original_price=55.00,
            group_size_max=16,
            difficulty="Moderate",
            rating=4.91,
            review_count=118,
            short_description="The ultimate student getaway! Riverside alpine dome tent camping by the Beas river, apple orchard trek to Jogini Waterfalls, Solang snow games, and cafe hopping in Old Manali.",
            detailed_overview="Designed for energetic college groups and young adventure-seekers. Stay right beside the crystal-clear Beas river in spacious alpine tents with sleeping bags. Trek to the cascading Jogini Waterfalls with breathtaking valley views, experience snow adventure in Solang Valley, and enjoy evening acoustic campfire sessions under starlit Himalayan skies.",
            image_url="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "Super budget-friendly ₹3,200 student package with riverside dome tent camping",
                "Acoustic campfire, barbecue snacks & music nights by the gushing Beas River",
                "Guided nature trek through pine woods & apple orchards to Jogini Waterfalls",
                "Solang Valley day trip with snow activities, zorbing and paragliding options",
                "Old Manali cafe exploration: live indie music, wood-fired pizzas & trout"
            ],
            included=[
                "2 nights alpine camping with warm sleeping bags & clean washrooms",
                "Daily camp breakfast & 2 hearty campfire dinners",
                "Local trekking leader for Jogini Waterfalls trail",
                "Shared transport coordination for Solang Valley"
            ],
            excluded=[
                "Bus tickets from Delhi/Chandigarh to Manali (Volvo ~₹800 - ₹1,100)",
                "Adventure sports charges (paragliding/ziplining) in Solang",
                "Cafe lunch and personal expenses"
            ],
            itinerary=[
                {"day": 1, "title": "Arrive in Manali & Riverside Campsite Check-in", "description": "Morning arrival at Manali bus stand. Transfer to your riverside campsite in Old Manali/Kullu valley. Freshen up, explore Hadimba Temple, and walk through bohemian Old Manali cafes. Evening campfire with music beside the Beas river."},
                {"day": 2, "title": "Jogini Waterfalls Nature Trek & Vashisht Hot Springs", "description": "Post breakfast, scenic trek past apple orchards and pine cliffs up to Jogini Waterfall. Take a refreshing dip in natural mountain water. Visit historic Vashisht village natural hot sulfur springs."},
                {"day": 3, "title": "Solang Valley Snow Point & Evening Departure", "description": "Day trip to Solang Valley for breathtaking views of snow-clad Himalayan peaks. Free afternoon on Mall Road for Tibetan souvenirs and street momos before catching the evening Volvo bus home."}
            ],
            upcoming_dates=["2026-05-08", "2026-05-22", "2026-06-12", "2026-07-10", "2026-08-14"],
            is_featured=True,
            is_trending=True
        )

        # --- MANALI: Luxury Chalet ($1,450 / ₹1,22,500) ---
        tour_manali_luxury = TourPackage.objects.create(
            destination=dest_manali,
            title="Manali Himalayan Luxury Chalet, Private Heli-Excursion & Lahaul",
            slug="manali-himalayan-luxury-chalet",
            category="Luxury",
            duration_days=5,
            travel_time="Private chartered helicopter from Chandigarh to Sissu/Manali (45 mins)",
            price_per_person=1450.00,
            original_price=1750.00,
            group_size_max=6,
            difficulty="Easy",
            rating=4.98,
            review_count=35,
            short_description="Exclusive 5-star private pine chalet with heated cedar jacuzzi, helicopter tour over Rohtang Pass, private 4x4 expedition through Atal Tunnel, and personal butler.",
            detailed_overview="An ultra-exclusive alpine retreat. Sleep in a hand-crafted cedarwood estate with roaring fireplaces and panoramic views of snow-crested peaks. Fly over the Rohtang Pass in a private helicopter and cross the world's longest high-altitude tunnel into the remote, barren desert beauty of Lahaul Valley.",
            image_url="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[],
            highlights=[
                "Private helicopter scenic flight over Rohtang Pass glaciers and Chandra river",
                "5-star private cedarwood chalet with personal chef and outdoor heated jacuzzi",
                "Private 4x4 Land Cruiser expedition to Sissu waterfall and Keylong in Lahaul",
                "Curated 5-course gourmet Himalayan fusion dinners paired with vintage wines"
            ],
            included=[
                "4 nights in private luxury chalet with mountain views",
                "Private butler and chef preparing tailored multi-course meals",
                "Chartered helicopter scenic flight",
                "Dedicated 4x4 luxury SUV throughout"
            ],
            excluded=[
                "International/domestic flights to Chandigarh",
                "Discretionary tips for chalet staff"
            ],
            itinerary=[
                {"day": 1, "title": "Helicopter Arrival & Chalet Champagne Welcome", "description": "Board private helicopter in Chandigarh. Touch down in Manali with champagne welcome at your private estate. Sunset jacuzzi session."},
                {"day": 2, "title": "Atal Tunnel & Moonscape of Lahaul", "description": "Chauffeured 4x4 drive through Atal Tunnel (9.02 km) to Sissu. Gourmet picnic beside the Sissu waterfall in Lahaul."},
                {"day": 3, "title": "Rohtang Glacier Heli-Tour", "description": "Morning helicopter flight landing on high glacier fields with panoramic views of Pir Panjal and Great Himalayan ranges."},
                {"day": 4, "title": "Naggar Castle Heritage & Artisan Trout Masterclass", "description": "Visit historic Naggar Castle and Nicholas Roerich art estate. Fresh Himalayan river trout masterclass by your private chef."},
                {"day": 5, "title": "Farewell Himalayas", "description": "Morning yoga overlooking apple orchards, champagne breakfast, and helicopter transfer back to Chandigarh."}
            ],
            upcoming_dates=["2026-05-15", "2026-06-18", "2026-07-20", "2026-09-25"],
            is_featured=False,
            is_trending=True
        )

        # --- MEGHALAYA: Student Backpacker (₹4,500 / $54) ---
        tour_meghalaya_student = TourPackage.objects.create(
            destination=dest_meghalaya,
            title="Meghalaya Backpacker Living Root Bridges & Dawki Crystal River",
            slug="meghalaya-backpacker-root-bridges",
            category="Student",
            duration_days=4,
            travel_time="3 hours shared cab from Guwahati Airport / Railway Station (GAU) to Shillong",
            price_per_person=53.25,  # Exact ₹4,500 INR @ 84.5 rate
            original_price=75.00,
            group_size_max=14,
            difficulty="Moderate",
            rating=4.95,
            review_count=87,
            short_description="Trek 3,500 steps down to the mystical Double Decker Living Root Bridge in Nongriat, swim in turquoise Rainbow Falls lagoons, boat on glass-clear Dawki river, and stay in Khasi homestays.",
            detailed_overview="A bucket-list Northeast India expedition built for student adventurers. Hike through dense emerald jungle gorges down to the world-famous bio-engineered Double Decker Living Root Bridge. Swim in natural azure river pools, kayak on the crystal-clear waters of the Umngot River where boats appear to float on air, and immerse yourself in matrilineal Khasi tribal culture.",
            image_url="https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "Unbeatable ₹4,500 budget expedition covering Shillong, Cherrapunji, Nongriat & Dawki",
                "Trek down 3,500 stone stairs into the tropical gorge of Double Decker Living Root Bridge",
                "Swim in natural blue lagoons beneath the thunderous Rainbow Falls",
                "Boating on the glass-like crystal clear Dawki river along the Bangladesh border",
                "Stay in traditional Khasi village eco-homestays with home-cooked organic meals"
            ],
            included=[
                "3 nights accommodation (2 nights eco-homestays in Nongriat & 1 night in Shillong)",
                "Daily wholesome local breakfasts and 2 village dinners",
                "Local Khasi jungle trek guide for root bridges",
                "Shared transport between Guwahati, Shillong, Cherrapunji and Dawki"
            ],
            excluded=[
                "Airfare/train to Guwahati",
                "Boat ride charges at Dawki (approx. ₹150-₹200 shared)",
                "Personal snacks and mineral water"
            ],
            itinerary=[
                {"day": 1, "title": "Guwahati to Shillong & Umiam Lake", "description": "Meet at Guwahati railway station/airport. Scenic drive up Khasi hills stopping at tranquil Umiam Lake. Check into Shillong hostel. Stroll through Police Bazaar for momos and live music."},
                {"day": 2, "title": "Descent to Double Decker Living Root Bridge", "description": "Early drive to Tyrna village. Begin the legendary trek down 3,500 stone stairs crossing suspension bridges over turquoise rivers. Arrive at Nongriat and marvel at the 250-year-old living root bridge. Overnight in village homestay."},
                {"day": 3, "title": "Rainbow Falls & Dawki Transparent Waters", "description": "Morning hike to the roaring Rainbow Falls. Ascend back to Tyrna and drive to Dawki. Marvel at the crystal-clear Umngot river where boats appear to float on air. Camp on river beach."},
                {"day": 4, "title": "Mawlynnong Cleanest Village & Guwahati Drop", "description": "Visit Mawlynnong, celebrated as the cleanest village in Asia. Walk on a single root bridge and transfer back to Guwahati for evening flight or train."}
            ],
            upcoming_dates=["2026-05-12", "2026-06-02", "2026-07-08", "2026-09-15", "2026-10-10"],
            is_featured=True,
            is_trending=True
        )

        # --- MEGHALAYA: Luxury Eco-Chalet ($1,280 / ₹1,08,000) ---
        tour_meghalaya_luxury = TourPackage.objects.create(
            destination=dest_meghalaya,
            title="Meghalaya Cloud-Realm Luxury Waterfall Retreat & Private Cave Safari",
            slug="meghalaya-cloud-realm-luxury-retreat",
            category="Luxury",
            duration_days=6,
            travel_time="Chauffeured luxury SUV from Guwahati Airport (approx. 2.5 hrs to Shillong)",
            price_per_person=1280.00,
            original_price=1500.00,
            group_size_max=8,
            difficulty="Easy",
            rating=4.96,
            review_count=31,
            short_description="Experience the luxury of the clouds: 5-star cliff-edge retreat overlooking Seven Sisters waterfalls, private cave explorations with speleologist, and VIP Dawki cruise.",
            detailed_overview="A refined, serene passage through Meghalaya's cloud-kissed canyons. Indulge in private cliffside suites facing thunderous plunging waterfalls, explore illuminated limestone caves with personal speleologists, and glide along private secluded reaches of the emerald Dawki river.",
            image_url="https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[],
            highlights=[
                "5 nights in premier luxury cliff-edge villas with waterfall views",
                "Private guided cave exploration with specialized lighting & safety gear",
                "Private chartered mahogany boat with gourmet champagne picnic in Dawki",
                "Helicopter transfer option from Guwahati directly to Shillong"
            ],
            included=[
                "5 nights luxury accommodation",
                "All chef-curated meals & private afternoon teas",
                "Chauffeured luxury SUV throughout",
                "Dedicated botanical & cultural guide"
            ],
            excluded=[
                "Airfare to Guwahati",
                "Personal alcoholic beverages and tips"
            ],
            itinerary=[
                {"day": 1, "title": "Guwahati to Shillong Heritage Resort", "description": "VIP pickup in Guwahati. Check into Ri Kynjai boutique resort on the banks of Umiam Lake."},
                {"day": 2, "title": "Shillong Golf Course & Khasi Cultural Masterclass", "description": "Morning stroll on historic natural 18-hole golf course. Private meeting with Khasi music and textile masters."},
                {"day": 3, "title": "Cherrapunji Canyon & Nohkalikai Falls Panorama", "description": "Drive across misty plateaus to Cherrapunji. Settle into clifftop villa overlooking the Seven Sisters waterfalls."},
                {"day": 4, "title": "Private Cave Exploration & Root Bridge Viewing", "description": "Explore pristine Mawsmai and Arwah limestone caves with resident geologist. Helicopter viewing of remote root bridges."},
                {"day": 5, "title": "Dawki Emerald River & Private Island Picnic", "description": "Private chartered boat ride on crystal waters with riverside barbecue lunch. Sunset drive back to Shillong."},
                {"day": 6, "title": "Farewell Abode of Clouds", "description": "Breakfast overlooking pine forests, transfer to Guwahati airport."}
            ],
            upcoming_dates=["2026-05-18", "2026-06-25", "2026-07-20", "2026-10-05"],
            is_featured=False,
            is_trending=False
        )

        # --- Existing International Tours (Amalfi, Kyoto, Swiss Alps) ---
        tour_amalfi = TourPackage.objects.create(
            destination=dest_amalfi,
            title="Amalfi Coast Cliffside Villa & Private Yacht Voyage",
            slug="amalfi-cliffside-yacht-voyage",
            category="Luxury",
            duration_days=7,
            travel_time="Approx. 1.5 hrs private Mercedes chauffeur from Naples Airport (NAP)",
            price_per_person=2450.00,
            original_price=2890.00,
            group_size_max=8,
            difficulty="Easy",
            rating=4.95,
            review_count=48,
            short_description="Experience quintessential Italian dolce vita with cliffside boutique stays, private Capri yacht cruises, and Michelin dining.",
            detailed_overview="Sail past soaring limestone cliffs, dive into the emerald waters of Capri's secret grottos, and stroll through Positano's charming bougainvillea-lined pathways.",
            image_url="https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "Full-day private wooden Riva boat cruise around Capri and Faraglioni rocks",
                "5-star cliffside boutique hotel with panoramic Mediterranean sea views",
                "Hands-on limoncello and handmade pasta masterclass at a Ravello family estate"
            ],
            included=[
                "6 nights in 5-star seaside boutique hotels",
                "Daily artisanal breakfast & 4 gourmet dinners",
                "Private luxury Mercedes chauffeur transfers",
                "Chartered yacht to Capri with champagne"
            ],
            excluded=[
                "International flights to Naples (NAP)",
                "Personal shopping & unlisted drinks"
            ],
            itinerary=[
                {"day": 1, "title": "Naples to Positano", "description": "Arrival, private chauffeur transfer, welcome sunset cocktail."},
                {"day": 2, "title": "Positano Artisans & Path of the Gods", "description": "Guided walking tour and scenic coastal hike."},
                {"day": 3, "title": "Private Capri Yacht Cruise", "description": "Sail to Capri, explore grottos, and cliffside dining."},
                {"day": 4, "title": "Ravello Gardens & Classical Music", "description": "Villa Rufolo gardens and private wine tasting."},
                {"day": 5, "title": "Amalfi Maritime Republic", "description": "St. Andrew cathedral and organic lemon orchards."},
                {"day": 6, "title": "Leisure & Gala Farewell Dinner", "description": "5-course celebration dinner with Campania wines."},
                {"day": 7, "title": "Arrivederci Amalfi", "description": "Private transfer to Naples airport or train station."}
            ],
            upcoming_dates=["2026-05-18", "2026-06-12", "2026-07-10"],
            is_featured=True,
            is_trending=True
        )

        tour_kyoto = TourPackage.objects.create(
            destination=dest_kyoto,
            title="Kyoto Zen Sanctuaries, Tea Ceremonies & Fuji Vista",
            slug="kyoto-zen-fuji-sanctuaries",
            category="Cultural",
            duration_days=8,
            travel_time="Direct high-speed Shinkansen Bullet Train from Tokyo (2 hrs) or Kansai Airport (1.2 hrs)",
            price_per_person=2190.00,
            original_price=2490.00,
            group_size_max=10,
            difficulty="Easy",
            rating=4.98,
            review_count=62,
            short_description="Immerse in Japanese heritage: ancient shrines, private tea masters, bamboo forests, and tranquil onsen baths overlooking Fuji.",
            detailed_overview="A serene spiritual passage through Kyoto, Nara, and Hakone. Experience traditional ryokan hospitality with seasonal multi-course Kaiseki dinners.",
            image_url="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
            gallery_urls=[
                "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=800&q=80"
            ],
            highlights=[
                "Exclusive morning access to Fushimi Inari torii gates before crowds",
                "Authentic tea ceremony led by an 8th-generation Uji tea master",
                "2 nights in a premier luxury onsen ryokan overlooking Mount Fuji"
            ],
            included=[
                "7 nights in luxury boutique hotels and authentic Ryokans",
                "Daily Japanese breakfast & 5 Kaiseki dinners",
                "All Shinkansen bullet train transfers",
                "Licensed National Tour Guide"
            ],
            excluded=[
                "International flights to Japan",
                "Personal expenses"
            ],
            itinerary=[
                {"day": 1, "title": "Arrive in Kyoto", "description": "Arrival, Gion orientation walk."},
                {"day": 2, "title": "Golden Pavilion & Bamboo Forest", "description": "Kinkaku-ji and Arashiyama."},
                {"day": 3, "title": "Torii Gates & Tea Ceremony", "description": "Fushimi Inari and Uji master tea estate."},
                {"day": 4, "title": "Nara Deer & Giant Buddha", "description": "Sacred deer park and Todaiji."},
                {"day": 5, "title": "Bullet Train to Hakone", "description": "Ryokan check-in and volcanic onsen."},
                {"day": 6, "title": "Mount Fuji Lake Ashi Cruise", "description": "Panoramic mountain boat cruise."},
                {"day": 7, "title": "Hakone Sculpture Park", "description": "Open-air art and farewell banquet."},
                {"day": 8, "title": "Sayonara Japan", "description": "Bullet train to Tokyo or airport."}
            ],
            upcoming_dates=["2026-05-02", "2026-06-15", "2026-09-20"],
            is_featured=True,
            is_trending=True
        )

        # ---------------------------------------------------------------------
        # 3. REVIEWS
        # ---------------------------------------------------------------------
        Review.objects.create(
            tour=tour_shimla_student,
            author_name="Rohit Sharma (Delhi University)",
            author_avatar="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=150&q=80",
            author_country="India",
            travel_type="Friends",
            rating=5,
            title="Completed the whole Shimla trip in exactly ₹2,000!",
            comment="As a college student, this was the best weekend trip ever! The hostel near Mall Road had a jaw-dropping mountain view terrace. The Jakhoo trek in the morning mist was surreal, and the siddu street food was delicious. Super legit budget pricing!"
        )

        Review.objects.create(
            tour=tour_manali_student,
            author_name="Pooja Verma (IIT Roorkee)",
            author_avatar="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80",
            author_country="India",
            travel_type="Friends",
            rating=5,
            title="Riverside camping in Manali under ₹3,500!",
            comment="The Beas river campfire with guitar music was the highlight of our semester break. Trekking to Jogini waterfalls was straight out of a movie. Amazing value for money!"
        )

        Review.objects.create(
            tour=tour_meghalaya_student,
            author_name="Ananya Sen (Jadavpur Univ)",
            author_avatar="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=150&q=80",
            author_country="India",
            travel_type="Solo",
            rating=5,
            title="The Living Root Bridge and Dawki exceeded all expectations",
            comment="Dawki river really is crystal clear like glass. Trekking 3,500 steps to the Double Decker root bridge was adventurous, and staying in the Khasi village homestay felt so warm and authentic. Unbelievable student budget trip!"
        )

        # ---------------------------------------------------------------------
        # 4. INITIAL SAMPLE BOOKINGS
        # ---------------------------------------------------------------------
        booking_student = Booking.objects.create(
            tour=tour_shimla_student,
            customer_name="Aman Gupta",
            customer_email="aman.student@example.com",
            customer_phone="+91 98765 43210",
            departure_date="2026-05-16",
            guests_count=1,
            price_per_person=23.67,
            selected_addons=[],
            total_price=23.67,
            special_requests="Traveling on student ID. Would like top bunk bed facing the mountains.",
            status="CONFIRMED"
        )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {Destination.objects.count()} destinations (including Shimla, Manali, Meghalaya) "
            f"and {TourPackage.objects.count()} tours (from ₹2,000 student deals to luxury retreats). "
            f"Sample Student Booking Code: {booking_student.booking_reference}"
        ))
