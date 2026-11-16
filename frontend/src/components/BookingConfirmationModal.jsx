import React from 'react';
import { CheckCircle2, Calendar, MapPin, Users, Printer, X, Ticket, ShieldCheck, Download } from 'lucide-react';
import { useTravel } from '../context/TravelContext';

export default function BookingConfirmationModal({ booking, onClose, onViewMyBookings }) {
  const { formatPrice } = useTravel();

  if (!booking) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        id="booking-confirmation-modal"
        className="modal-content animate-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '680px', overflow: 'hidden' }}
      >
        {/* Success Banner */}
        <div style={{
          background: 'linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)',
          color: '#ffffff',
          padding: '2rem 2rem 1.5rem 2rem',
          textAlign: 'center',
          position: 'relative'
        }}>
          <button
            id="btn-close-confirmation"
            onClick={onClose}
            aria-label="Close"
            style={{
              position: 'absolute',
              top: '1rem',
              right: '1rem',
              background: 'rgba(255,255,255,0.2)',
              border: 'none',
              borderRadius: '50%',
              width: '32px',
              height: '32px',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>

          <div style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: 'rgba(255,255,255,0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem auto'
          }}>
            <CheckCircle2 size={36} color="#ffffff" />
          </div>

          <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ffffff', marginBottom: '0.4rem' }}>
            Reservation Confirmed!
          </h2>
          <p style={{ fontSize: '0.95rem', opacity: 0.9 }}>
            Your expedition has been reserved. A confirmation pack has been sent to <strong>{booking.customer_email}</strong>.
          </p>
        </div>

        {/* Boarding Pass / Ticket Card */}
        <div style={{ padding: '2rem' }}>
          <div style={{
            border: '2px dashed var(--border-medium)',
            borderRadius: 'var(--radius-lg)',
            padding: '1.5rem',
            background: 'var(--bg-card-subtle)',
            position: 'relative'
          }}>
            {/* Top Reference & Status */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderBottom: '1px solid var(--border-light)',
              paddingBottom: '1rem',
              marginBottom: '1.25rem'
            }}>
              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, color: 'var(--text-muted)' }}>
                  Booking Reference
                </span>
                <div style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--primary)', letterSpacing: '0.05em' }}>
                  {booking.booking_reference}
                </div>
              </div>
              <div style={{
                background: 'rgba(20, 184, 166, 0.15)',
                color: 'var(--primary)',
                fontWeight: 700,
                fontSize: '0.8rem',
                padding: '0.35rem 0.85rem',
                borderRadius: 'var(--radius-full)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem'
              }}>
                <ShieldCheck size={16} />
                <span>CONFIRMED & GUARANTEED</span>
              </div>
            </div>

            {/* Tour info */}
            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                Expedition Title
              </div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-main)', marginTop: '2px' }}>
                {booking.tour_title || 'Curated Expedition Journey'}
              </div>
            </div>

            {/* Grid details */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
              gap: '1rem',
              marginBottom: '1.25rem'
            }}>
              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                  Lead Guest
                </span>
                <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                  {booking.customer_name}
                </div>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                  Departure Date
                </span>
                <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <Calendar size={14} style={{ color: 'var(--primary)' }} />
                  {booking.departure_date}
                </div>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                  Party Size
                </span>
                <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                  <Users size={14} style={{ color: 'var(--secondary)' }} />
                  {booking.guests_count} {booking.guests_count === 1 ? 'Guest' : 'Guests'}
                </div>
              </div>

              <div>
                <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>
                  Total Paid
                </span>
                <div style={{ fontWeight: 800, fontSize: '1.1rem', color: 'var(--primary)', fontFamily: 'var(--font-heading)' }}>
                  {formatPrice(booking.total_price)}
                </div>
              </div>
            </div>

            {/* Addons if any */}
            {booking.selected_addons && booking.selected_addons.length > 0 && (
              <div style={{
                background: 'var(--bg-card)',
                padding: '0.75rem 1rem',
                borderRadius: 'var(--radius-md)',
                marginBottom: '1rem',
                fontSize: '0.82rem'
              }}>
                <span style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '0.7rem' }}>
                  Included Special Upgrades:
                </span>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.25rem' }}>
                  {booking.selected_addons.map((add, idx) => (
                    <span key={idx} className="badge badge-category">
                      ✓ {typeof add === 'string' ? add : add.name}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Decorative Barcode */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              paddingTop: '0.75rem',
              borderTop: '1px solid var(--border-light)',
              opacity: 0.7
            }}>
              <div style={{
                fontFamily: 'monospace',
                letterSpacing: '0.35em',
                fontSize: '0.7rem',
                color: 'var(--text-muted)'
              }}>
                ||| | ||||| || |||||| | ||||| |||| | ||| ||||||| | |||
              </div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                DIGITAL PASS IDENTIFIER • {booking.booking_reference} • BOOKWITHGULSHAN EXCLUSIVE
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1rem',
            marginTop: '1.5rem',
            flexWrap: 'wrap'
          }}>
            <button
              id="btn-print-confirmation"
              onClick={handlePrint}
              className="btn-secondary"
              style={{ gap: '0.5rem', fontSize: '0.88rem' }}
            >
              <Printer size={16} />
              <span>Print Boarding Ticket</span>
            </button>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                id="btn-view-in-my-bookings"
                onClick={() => {
                  onClose();
                  onViewMyBookings(booking.booking_reference);
                }}
                className="btn-secondary"
                style={{ fontSize: '0.88rem', gap: '0.4rem' }}
              >
                <Ticket size={16} style={{ color: 'var(--primary)' }} />
                <span>My Bookings</span>
              </button>
              <button
                id="btn-done-confirmation"
                onClick={onClose}
                className="btn-primary"
                style={{ fontSize: '0.88rem', padding: '0.65rem 1.5rem' }}
              >
                Done
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
