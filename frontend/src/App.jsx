import React, { useState, useEffect } from 'react';
import { TravelProvider, useTravel } from './context/TravelContext';
import { api } from './services/api';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import DestinationPills from './components/DestinationPills';
import FilterBar from './components/FilterBar';
import TourCard from './components/TourCard';
import TourDetailModal from './components/TourDetailModal';
import BookingModal from './components/BookingModal';
import BookingConfirmationModal from './components/BookingConfirmationModal';
import MyBookingsModal from './components/MyBookingsModal';
import WishlistModal from './components/WishlistModal';
import Footer from './components/Footer';
import { Sparkles, Compass, AlertCircle, RefreshCw } from 'lucide-react';

function BookingPlatformContent() {
  const [destinations, setDestinations] = useState([]);
  const [tours, setTours] = useState([]);
  const [allTours, setAllTours] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active filter state
  const [activeDestinationId, setActiveDestinationId] = useState(null);
  const [filters, setFilters] = useState({
    category: 'All',
    search: '',
    difficulty: 'All',
    max_price: 4000,
    sort: 'featured',
  });

  // Modal states
  const [detailTourId, setDetailTourId] = useState(null);
  const [bookingTour, setBookingTour] = useState(null);
  const [confirmedBooking, setConfirmedBooking] = useState(null);
  const [showMyBookings, setShowMyBookings] = useState(false);
  const [lookupBookingRef, setLookupBookingRef] = useState('');
  const [showWishlist, setShowWishlist] = useState(false);

  // Load initial static data (destinations & stats)
  useEffect(() => {
    Promise.all([
      api.getDestinations().catch(() => []),
      api.getStats().catch(() => null),
      api.getTrips().catch(() => [])
    ]).then(([dests, platformStats, allToursList]) => {
      setDestinations(dests);
      setStats(platformStats);
      setAllTours(allToursList);
    });
  }, []);

  // Fetch filtered trips whenever filters or activeDestination change
  useEffect(() => {
    setLoading(true);
    setError(null);

    const queryParams = {
      ...filters,
      destination: activeDestinationId || '',
    };

    api.getTrips(queryParams)
      .then(data => {
        setTours(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Failed to load expeditions');
        setLoading(false);
      });
  }, [filters, activeDestinationId]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleResetFilters = () => {
    setActiveDestinationId(null);
    setFilters({
      category: 'All',
      search: '',
      difficulty: 'All',
      max_price: 4000,
      sort: 'featured',
    });
  };

  const handleHeroSearch = ({ search, destination, category }) => {
    setActiveDestinationId(destination ? Number(destination) : null);
    setFilters(prev => ({
      ...prev,
      search: search || '',
      category: category || 'All',
    }));

    // Scroll smoothly to catalog
    const catalogElement = document.getElementById('catalog');
    if (catalogElement) {
      catalogElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleNavigateSection = (sectionId) => {
    if (sectionId === 'hero') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  const handleOpenMyBookingsWithRef = (ref) => {
    setLookupBookingRef(ref || '');
    setShowMyBookings(true);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Navigation */}
      <Navbar
        onOpenMyBookings={() => handleOpenMyBookingsWithRef('')}
        onOpenWishlist={() => setShowWishlist(true)}
        onNavigateSection={handleNavigateSection}
      />

      <main style={{ flexGrow: 1 }}>
        {/* Hero Section */}
        <HeroSection
          destinations={destinations}
          onSearchSubmit={handleHeroSearch}
          stats={stats}
        />

        {/* Destination Explorer Pills */}
        <DestinationPills
          destinations={destinations}
          activeDestinationId={activeDestinationId}
          onSelectDestination={setActiveDestinationId}
        />

        {/* Tour Catalog & Filter Section */}
        <section id="catalog" style={{ padding: '2.5rem 0 4rem 0' }}>
          <div className="container">
            {/* Catalog Section Heading */}
            <div style={{ marginBottom: '1.75rem' }}>
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.4rem',
                fontSize: '0.8rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: 'var(--primary)',
                marginBottom: '0.35rem'
              }}>
                <Sparkles size={16} />
                <span>Handpicked Itineraries</span>
              </div>
              <h2 style={{ fontSize: '2.2rem', fontWeight: 800 }}>
                Curated Travel Expeditions
              </h2>
            </div>

            {/* Filter Bar */}
            <FilterBar
              filters={filters}
              onFilterChange={handleFilterChange}
              onResetFilters={handleResetFilters}
              totalResults={tours.length}
            />

            {/* Catalog Grid / States */}
            {loading ? (
              <div style={{
                textAlign: 'center',
                padding: '5rem 0',
                color: 'var(--text-muted)'
              }}>
                <div className="animate-spin-slow" style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🧭</div>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
                  Loading Expeditions...
                </h3>
                <p style={{ fontSize: '0.9rem' }}>Matching bespoke journeys to your criteria</p>
              </div>
            ) : error ? (
              <div style={{
                textAlign: 'center',
                padding: '4rem 1.5rem',
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius-xl)',
                border: '1px solid var(--border-light)'
              }}>
                <AlertCircle size={40} style={{ color: '#ef4444', marginBottom: '1rem' }} />
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                  Unable to load tours
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                  {error}
                </p>
                <button
                  onClick={handleResetFilters}
                  className="btn-primary"
                  style={{ gap: '0.5rem' }}
                >
                  <RefreshCw size={16} />
                  <span>Retry & Reset Filters</span>
                </button>
              </div>
            ) : tours.length === 0 ? (
              <div style={{
                textAlign: 'center',
                padding: '4.5rem 1.5rem',
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius-xl)',
                border: '1px solid var(--border-light)'
              }}>
                <Compass size={48} style={{ opacity: 0.3, marginBottom: '1rem', color: 'var(--primary)' }} />
                <h3 style={{ fontSize: '1.35rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                  No Expeditions Found
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '460px', margin: '0 auto 1.5rem auto' }}>
                  We couldn't find any tours matching all your selected filters. Try broadening your budget range or resetting criteria.
                </p>
                <button
                  id="btn-empty-reset"
                  onClick={handleResetFilters}
                  className="btn-primary"
                >
                  Reset All Filters
                </button>
              </div>
            ) : (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
                gap: '2rem'
              }}>
                {tours.map(tour => (
                  <TourCard
                    key={tour.id}
                    tour={tour}
                    onOpenDetail={(id) => setDetailTourId(id)}
                    onBookNow={(t) => setBookingTour(t)}
                  />
                ))}
              </div>
            )}
          </div>
        </section>

        {/* Reviews Section Anchor */}
        <section id="reviews" style={{
          padding: '4rem 0',
          background: 'var(--bg-card-subtle)',
          borderTop: '1px solid var(--border-light)',
          borderBottom: '1px solid var(--border-light)'
        }}>
          <div className="container">
            <div style={{ textAlign: 'center', maxWidth: '700px', margin: '0 auto 3rem auto' }}>
              <div style={{
                fontSize: '0.8rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: 'var(--primary)',
                marginBottom: '0.25rem'
              }}>
                Traveller Reviews
              </div>
              <h2 style={{ fontSize: '2.1rem', fontWeight: 800, marginBottom: '0.75rem' }}>
                Cherished Stories from the Field
              </h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '1.05rem' }}>
                Hear from explorers who ventured with us into secret Mediterranean grottos,
                serene Kyoto shrines, and wild African savannahs.
              </p>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
              gap: '1.5rem'
            }}>
              {/* Feature review 1 */}
              <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: 'var(--radius-lg)' }}>
                <div style={{ display: 'flex', gap: '3px', color: 'var(--accent)', marginBottom: '0.75rem' }}>
                  ★★★★★
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                  "The Capri private yacht cruise was unreal"
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                  "Booking on bookwithgulshan was flawless. When our boat sailed around the Faraglioni rocks with chilled champagne, I knew we had made the right choice. Seamless execution from start to finish."
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <img
                    src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=100&q=80"
                    alt="Sophia M."
                    style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                  />
                  <div>
                    <strong style={{ fontSize: '0.9rem' }}>Sophia Montgomery</strong>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Amalfi Cliffside Expedition • UK</div>
                  </div>
                </div>
              </div>

              {/* Feature review 2 */}
              <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: 'var(--radius-lg)' }}>
                <div style={{ display: 'flex', gap: '3px', color: 'var(--accent)', marginBottom: '0.75rem' }}>
                  ★★★★★
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                  "Sacred dawn in Kyoto without crowds"
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                  "Our guide arranged private temple access at 6 AM before anyone else arrived. The Ryokan in Hakone with cedar hot springs overlooking Mount Fuji was the most restorative experience."
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <img
                    src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80"
                    alt="Elena R."
                    style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                  />
                  <div>
                    <strong style={{ fontSize: '0.9rem' }}>Elena Rostova</strong>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Kyoto Zen Sanctuaries • Canada</div>
                  </div>
                </div>
              </div>

              {/* Feature review 3 */}
              <div className="glass-panel" style={{ padding: '1.75rem', borderRadius: 'var(--radius-lg)' }}>
                <div style={{ display: 'flex', gap: '3px', color: 'var(--accent)', marginBottom: '0.75rem' }}>
                  ★★★★★
                </div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                  "Saw all Big Five on day three in Tanzania"
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1.25rem' }}>
                  "Drifting over the Serengeti at sunrise in a hot air balloon, followed by a champagne bush breakfast, exceeded every dream. The luxury tented camps were 5-star."
                </p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <img
                    src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=100&q=80"
                    alt="Marcus V."
                    style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }}
                  />
                  <div>
                    <strong style={{ fontSize: '0.9rem' }}>Marcus Vance</strong>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Serengeti Great Migration • USA</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <Footer onNavigateSection={handleNavigateSection} />

      {/* Modals & Overlays */}
      {detailTourId && (
        <TourDetailModal
          tourId={detailTourId}
          onClose={() => setDetailTourId(null)}
          onBookTour={(t) => {
            setDetailTourId(null);
            setBookingTour(t);
          }}
        />
      )}

      {bookingTour && (
        <BookingModal
          tour={bookingTour}
          onClose={() => setBookingTour(null)}
          onBookingSuccess={(newBooking) => {
            setBookingTour(null);
            setConfirmedBooking(newBooking);
          }}
        />
      )}

      {confirmedBooking && (
        <BookingConfirmationModal
          booking={confirmedBooking}
          onClose={() => setConfirmedBooking(null)}
          onViewMyBookings={(ref) => {
            setConfirmedBooking(null);
            handleOpenMyBookingsWithRef(ref);
          }}
        />
      )}

      {showMyBookings && (
        <MyBookingsModal
          initialReference={lookupBookingRef}
          onClose={() => {
            setShowMyBookings(false);
            setLookupBookingRef('');
          }}
          onSelectBookingForView={(bookingItem) => {
            setShowMyBookings(false);
            setConfirmedBooking(bookingItem);
          }}
        />
      )}

      {showWishlist && (
        <WishlistModal
          tours={allTours.length > 0 ? allTours : tours}
          onClose={() => setShowWishlist(false)}
          onOpenDetail={(id) => {
            setShowWishlist(false);
            setDetailTourId(id);
          }}
          onBookNow={(t) => {
            setShowWishlist(false);
            setBookingTour(t);
          }}
        />
      )}
    </div>
  );
}

export default function App() {
  return (
    <TravelProvider>
      <BookingPlatformContent />
    </TravelProvider>
  );
}
