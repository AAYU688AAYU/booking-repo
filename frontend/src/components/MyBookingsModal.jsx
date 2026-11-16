import React, { useState, useEffect } from 'react';
import { X, Search, Ticket, Calendar, Users, ShieldCheck, AlertCircle, ArrowRight } from 'lucide-react';
import { useTravel } from '../context/TravelContext';
import { api } from '../services/api';

export default function MyBookingsModal({ initialReference, onClose, onSelectBookingForView }) {
  const { formatPrice, myBookingRefs } = useTravel();
  const [searchQuery, setSearchQuery] = useState(initialReference || '');
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState('');

  const fetchBookings = async (queryToUse) => {
    const q = queryToUse !== undefined ? queryToUse : searchQuery;
    if (!q.trim()) return;

    setLoading(true);
    setError('');
    setSearched(true);

    try {
      const isEmail = q.includes('@');
      const params = isEmail ? { email: q.trim() } : { reference: q.trim() };
      const data = await api.getBookings(params);
      setBookings(data);
    } catch (err) {
      setError(err.message || 'Unable to retrieve reservations.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialReference) {
      fetchBookings(initialReference);
    } else if (myBookingRefs && myBookingRefs.length > 0) {
      // Auto-fetch using the most recent booking ref
      fetchBookings(myBookingRefs[0]);
    }
  }, [initialReference]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchBookings();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        id="my-bookings-modal"
        className="modal-content animate-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '720px' }}
      >
        {/* Header */}
        <div style={{
          padding: '1.25rem 1.75rem',
          borderBottom: '1px solid var(--border-light)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--bg-card-subtle)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'var(--primary)',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Ticket size={20} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                My Travel Reservations
              </h3>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Track active departures, itinerary passes, and booking details
              </div>
            </div>
          </div>

          <button
            id="btn-close-my-bookings"
            onClick={onClose}
            aria-label="Close"
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--text-secondary)'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Search Bar inside Modal */}
        <div style={{ padding: '1.5rem 1.75rem 0.5rem 1.75rem' }}>
          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.5rem' }}>
            <div style={{
              flexGrow: 1,
              display: 'flex',
              alignItems: 'center',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-medium)',
              borderRadius: 'var(--radius-md)',
              padding: '0.5rem 0.85rem',
              gap: '0.5rem'
            }}>
              <Search size={18} style={{ color: 'var(--text-muted)' }} />
              <input
                id="input-lookup-booking"
                type="text"
                placeholder="Enter Booking Reference (e.g. TRV-30092) or Email"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  border: 'none',
                  background: 'transparent',
                  outline: 'none',
                  width: '100%',
                  fontSize: '0.9rem',
                  color: 'var(--text-main)',
                  fontWeight: 600
                }}
              />
            </div>
            <button
              id="btn-submit-booking-lookup"
              type="submit"
              className="btn-primary"
              style={{ padding: '0.5rem 1.25rem', fontSize: '0.88rem' }}
            >
              Lookup
            </button>
          </form>

          {/* Quick-test chips */}
          {myBookingRefs && myBookingRefs.length > 0 && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>Quick Lookups:</span>
              {myBookingRefs.slice(0, 4).map(ref => (
                <button
                  key={ref}
                  type="button"
                  onClick={() => {
                    setSearchQuery(ref);
                    fetchBookings(ref);
                  }}
                  style={{
                    padding: '0.2rem 0.6rem',
                    borderRadius: 'var(--radius-full)',
                    border: '1px solid var(--border-medium)',
                    background: 'var(--bg-card)',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    color: 'var(--primary)',
                    cursor: 'pointer'
                  }}
                >
                  {ref}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Results Area */}
        <div style={{ padding: '1.5rem 1.75rem', maxHeight: '55vh', overflowY: 'auto' }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-muted)' }}>
              <div className="animate-spin-slow" style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>🧭</div>
              <p>Fetching reservation records...</p>
            </div>
          ) : error ? (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '1rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(239, 68, 68, 0.1)',
              color: '#dc2626',
              fontSize: '0.88rem'
            }}>
              <AlertCircle size={18} />
              <span>{error}</span>
            </div>
          ) : bookings.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2.5rem', color: 'var(--text-secondary)' }}>
              <Ticket size={40} style={{ opacity: 0.3, marginBottom: '0.75rem' }} />
              <h4 style={{ fontWeight: 700, marginBottom: '0.25rem' }}>
                {searched ? 'No Reservations Found' : 'Search Your Reservations'}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', maxWidth: '380px', margin: '0 auto' }}>
                Enter your booking confirmation code (e.g. TRV-30092) or contact email above to retrieve your travel itinerary and boarding pass.
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {bookings.map(item => (
                <div
                  key={item.id}
                  id={`booking-item-${item.booking_reference}`}
                  style={{
                    padding: '1.25rem',
                    borderRadius: 'var(--radius-lg)',
                    border: '1px solid var(--border-light)',
                    background: 'var(--bg-card)',
                    boxShadow: 'var(--shadow-sm)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                      <span style={{
                        fontWeight: 800,
                        fontSize: '1.15rem',
                        color: 'var(--primary)',
                        letterSpacing: '0.05em'
                      }}>
                        {item.booking_reference}
                      </span>
                      <span className="badge" style={{
                        background: item.status === 'CONFIRMED' ? 'rgba(20, 184, 166, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                        color: item.status === 'CONFIRMED' ? 'var(--primary)' : 'var(--accent)'
                      }}>
                        ● {item.status}
                      </span>
                    </div>

                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      Booked for: <strong>{item.customer_name}</strong>
                    </span>
                  </div>

                  <div>
                    <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '0.2rem' }}>
                      {item.tour_title || 'Expedition Voyage'}
                    </h4>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      Destination: {item.tour_destination || 'Curated'}
                    </div>
                  </div>

                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1.5rem',
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)',
                    flexWrap: 'wrap',
                    padding: '0.6rem 0',
                    borderTop: '1px solid var(--border-light)',
                    borderBottom: '1px solid var(--border-light)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      <Calendar size={15} style={{ color: 'var(--primary)' }} />
                      <span>Departure: <strong>{item.departure_date}</strong></span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                      <Users size={15} style={{ color: 'var(--secondary)' }} />
                      <span>{item.guests_count} Guests</span>
                    </div>
                    <div style={{ marginLeft: 'auto', fontWeight: 800, color: 'var(--text-main)', fontSize: '1.05rem', fontFamily: 'var(--font-heading)' }}>
                      {formatPrice(item.total_price)}
                    </div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                    <button
                      id={`btn-view-pass-${item.booking_reference}`}
                      onClick={() => {
                        onClose();
                        onSelectBookingForView(item);
                      }}
                      className="btn-primary"
                      style={{ padding: '0.45rem 1rem', fontSize: '0.82rem', gap: '0.35rem' }}
                    >
                      <span>View Boarding Ticket</span>
                      <ArrowRight size={14} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
