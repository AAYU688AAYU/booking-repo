# VoyageCraft 🧭 — Luxury Experiential Travel & Booking Platform

A full-stack, modern travel booking platform designed for curating and booking world-class travel expeditions, cultural journeys, and scenic getaways. Built with a **React.js + Vite** frontend and a **Python Django REST Framework (DRF)** backend.

---

## 🌟 Key Features

### 🎨 Frontend (React.js + Vite)
- **Rich Visual Aesthetics**: Modern typography (Outfit & Plus Jakarta Sans), curated color palette (emerald teal, warm amber gold, deep slate), subtle micro-animations, and glassmorphism.
- **Hero Explorer**: Search tours by landmark/keyword, destination dropdown, and travel style.
- **Curated Destinations**: Interactive cards showcasing world destinations (Amalfi Coast, Kyoto & Mount Fuji, Swiss Alps, Bali, Serengeti, Patagonia, Santorini, Reykjavik).
- **Multi-Filter Engine**: Filter trips by category (Luxury, Cultural, Adventure, Wildlife, Relaxation), difficulty/pace, budget price slider, and sorting (price, rating, duration).
- **Interactive Day-by-Day Itineraries**: Expandable and collapsible day timeline breakdown with highlights and included/excluded amenities.
- **Dynamic Booking & Add-ons**:
  - Live price calculation based on passenger count and selected upgrades (e.g., VIP Airport Chauffeur, Suite Upgrade, Travel Protection).
  - Instant booking submission generating a unique reservation reference code (e.g., `TRV-18112`).
- **Digital Boarding Pass**:
  - Authentic boarding pass and travel ticket view with barcode identifier, guaranteed status badge, lead passenger details, and printable format (`window.print()`).
- **"My Bookings" Lookup Drawer**:
  - Instant ticket retrieval using booking reference code or email address.
- **Wishlist & Saved Expeditions**:
  - Save dream itineraries with local persistence and one-click booking.
- **Real-Time Currency Switcher**:
  - Real-time conversion across USD ($), EUR (€), GBP (£), INR (₹), and AUD (A$).
- **Dark / Light Mode**:
  - Toggle between luxury dark mode and clean daylight theme.

### ⚙️ Backend (Python + Django REST Framework)
- **Data Models**:
  - `Destination`: Name, country, region, climate, best season, hero imagery.
  - `TourPackage`: Title, slug, category, duration, price, max group size, difficulty, rating, reviews count, inclusions/exclusions, gallery, and day-by-day JSON itinerary.
  - `Booking`: Unique reference generator (`TRV-XXXXX`), lead contact info, departure date, guest count, calculated total, add-ons, and confirmation status.
  - `Review`: Star rating, travel style (Solo, Couple, Family, Friends), commentary, and automatic tour rating recalculation.
- **RESTful Endpoints**:
  - `GET /api/destinations/`: List all destinations with tour counts.
  - `GET /api/trips/`: List tours with query parameters (`search`, `category`, `destination`, `difficulty`, `min_price`, `max_price`, `sort`).
  - `GET /api/trips/<id>/`: Full detail for an expedition with nested reviews and day-by-day itinerary.
  - `POST /api/trips/<id>/reviews/`: Submit guest review and update average rating.
  - `POST /api/bookings/`: Create reservation with server-side price computation and unique reference generation.
  - `GET /api/bookings/`: Search bookings by `email` or `reference`.
  - `GET /api/bookings/<ref>/`: Retrieve single booking ticket by reference code.
  - `GET /api/stats/`: Platform overview statistics.
- **CORS Configured**: Ready for local and cross-origin frontend consumption.
- **Admin Dashboard**: Full CRUD management interface at `/admin/`.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ installed
- Node.js 18+ and npm installed

### 2. Automatic One-Step Startup
Simply run the root startup script:
```bash
./run.sh
```
This automatically starts both the Django API (`http://127.0.0.1:8000/`) and the Vite React frontend (`http://localhost:5173/`).

---

### 3. Manual Step-by-Step Setup

#### Backend Setup
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install django djangorestframework django-cors-headers

# 3. Apply migrations & seed initial travel packages
cd backend
python manage.py makemigrations api
python manage.py migrate
python manage.py seed_data

# 4. Start the Django dev server
python manage.py runserver 127.0.0.1:8000
```

#### Frontend Setup
```bash
# In a separate terminal:
cd frontend

# 1. Install dependencies
npm install

# 2. Start Vite development server
npm run dev
```

Open [http://localhost:5173/](http://localhost:5173/) in your browser.

---

## 🧪 Testing the API
You can test the endpoints directly via `curl`:

```bash
# 1. Fetch available tours
curl -s http://127.0.0.1:8000/api/trips/

# 2. Create a reservation
curl -X POST http://127.0.0.1:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "tour": 1,
    "customer_name": "Elena Rostova",
    "customer_email": "elena.rostova@example.com",
    "customer_phone": "+1 555-892-4102",
    "departure_date": "2026-06-12",
    "guests_count": 2,
    "selected_addons": [{"name": "VIP Private Chauffeur Airport Transfer", "price": 95}],
    "special_requests": "Ocean view room request"
  }'

# 3. Retrieve your booking boarding pass
curl -s http://127.0.0.1:8000/api/bookings/TRV-18112/
```

---

## 📂 Project Directory Structure

```
booking_plateform/
├── backend/                      # Django REST Framework backend
│   ├── booking_core/             # Project settings, wsgi, urls
│   │   ├── settings.py           # Installed apps, CORS, DRF configuration
│   │   └── urls.py               # Main URL router
│   ├── api/                      # Main API application
│   │   ├── models.py             # Destination, TourPackage, Booking, Review
│   │   ├── serializers.py        # DRF Serializers with calculation logic
│   │   ├── views.py              # List, detail, booking, review endpoints
│   │   ├── urls.py               # API route definitions
│   │   ├── admin.py              # Django admin registrations
│   │   └── management/commands/  # `seed_data` management command
│   ├── db.sqlite3                # SQLite database with sample destinations & tours
│   └── manage.py
├── frontend/                     # React.js + Vite application
│   ├── src/
│   │   ├── components/           # Navbar, Hero, TourCard, Modals, Footer
│   │   ├── context/              # TravelContext (currency, wishlist, theme)
│   │   ├── services/             # API client methods
│   │   ├── App.jsx               # Main application component
│   │   ├── index.css             # Design system tokens and styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js            # Vite configuration with DRF proxy
├── run.sh                        # All-in-one background runner
└── README.md
```
