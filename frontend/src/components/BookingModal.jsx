import React, { useState } from 'react';
import { X, Calendar, Users, Shield, Plus, Minus, CreditCard, Sparkles, AlertCircle } from 'lucide-react';
import { useTravel } from '../context/TravelContext';
import { api } from '../services/api';

const AVAILABLE_ADDONS = [
  { id: 'transfer', name: 'VIP Private Chauffeur Airport Transfer', price: 95, icon: '🚗' },
  { id: 'upgrade', name: 'Luxury Suite Upgrade with Panorama View', price: 250, icon: '✨' },
  { id: 'insurance', name: 'Comprehensive Expedition Travel Protection', price: 75, icon: '🛡️' },
];

export default function BookingModal({ tour, onClose, onBookingSuccess }) {
  const { formatPrice, addBookingRef } = useTravel();

  // Selected date defaults to first upcoming date
  const defaultDate = (tour?.upcoming_dates && tour.upcoming_dates.length > 0)
    ? tour.upcoming_dates[0]
    : '2026-06-15';

  const [departureDate, setDepartureDate] = useState(defaultDate);
  const [guestsCount, setGuestsCount] = useState(2);
  const [selectedAddons, setSelectedAddons] = useState([]);
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');
  const [customerPhone, setCustomerPhone] = useState('');
  const [specialRequests, setSpecialRequests] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  if (!tour) return null;

  const toggleAddon = (addon) => {
    setSelectedAddons(prev => {
      const exists = prev.some(a => a.name === addon.name);
      if (exists) {
        return prev.filter(a => a.name !== addon.name);
      } else {
        return [...prev, { name: addon.name, price: addon.price }];
      }
    });
  };

  // Price calculations
  const basePricePerPerson = parseFloat(tour.price_per_person) || 0;
  const addonsTotalPerPerson = selectedAddons.reduce((acc, curr) => acc + curr.price, 0);
  const grandTotal = (basePricePerPerson + addonsTotalPerPerson) * guestsCount;

  const handleIncrementGuests = () => {
    if (guestsCount < (tour.group_size_max || 12)) {
      setGuestsCount(guestsCount + 1);
    }
  };

  const handleDecrementGuests = () => {
    if (guestsCount > 1) {
      setGuestsCount(guestsCount - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!customerName || !customerEmail || !customerPhone) {
      setErrorMessage('Please complete all contact details.');
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        tour: tour.id,
        customer_name: customerName,
        customer_email: customerEmail,
        customer_phone: customerPhone,
        departure_date: departureDate,
        guests_count: guestsCount,
        selected_addons: selectedAddons,
        special_requests: specialRequests,
      };

      const result = await api.createBooking(payload);
      addBookingRef(result.booking_reference);
      onBookingSuccess(result);
    } catch (err) {
      setErrorMessage(err.message || 'Error completing booking. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        id="booking-modal"
        className="modal-content animate-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '780px' }}
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
          <div>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary)', textTransform: 'uppercase' }}>
              Confirm Reservation
            </div>
            <h3 style={{ fontSize: '1.35rem', fontWeight: 800 }}>
              {tour.title}
            </h3>
          </div>
          <button
            id="btn-close-booking-modal"
            onClick={onClose}
            aria-label="Close"
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--text-secondary)'
            }}
          >
            <X size={22} />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} style={{ padding: '1.75rem' }}>
          {errorMessage && (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(239, 68, 68, 0.1)',
              color: '#dc2626',
              marginBottom: '1.25rem',
              fontSize: '0.85rem'
            }}>
              <AlertCircle size={18} />
              <span>{errorMessage}</span>
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
            {/* Left column: Date & Guests */}
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Select Departure Date
              </label>
              <div style={{ position: 'relative', marginBottom: '1.25rem' }}>
                <select
                  id="booking-date-select"
                  value={departureDate}
                  onChange={(e) => setDepartureDate(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-medium)',
                    background: 'var(--bg-card)',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    color: 'var(--text-main)',
                    outline: 'none',
                    cursor: 'pointer'
                  }}
                >
                  {tour.upcoming_dates?.map((d, i) => (
                    <option key={i} value={d}>
                      {d} — Guaranteed Departure
                    </option>
                  ))}
                  <option value="2026-08-20">2026-08-20 — Late Summer Special</option>
                  <option value="2026-10-15">2026-10-15 — Autumn Foliage Expedition</option>
                </select>
              </div>

              {/* Guest counter */}
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Number of Travellers
              </label>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--border-medium)',
                background: 'var(--bg-card)',
                marginBottom: '1.25rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Users size={18} style={{ color: 'var(--primary)' }} />
                  <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                    {guestsCount} {guestsCount === 1 ? 'Guest' : 'Guests'}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <button
                    type="button"
                    id="btn-decrement-guests"
                    onClick={handleDecrementGuests}
                    disabled={guestsCount <= 1}
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card-subtle)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: guestsCount <= 1 ? 'not-allowed' : 'pointer'
                    }}
                  >
                    <Minus size={15} />
                  </button>
                  <span style={{ minWidth: '20px', textAlign: 'center', fontWeight: 700 }}>{guestsCount}</span>
                  <button
                    type="button"
                    id="btn-increment-guests"
                    onClick={handleIncrementGuests}
                    disabled={guestsCount >= (tour.group_size_max || 12)}
                    style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card-subtle)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: guestsCount >= (tour.group_size_max || 12) ? 'not-allowed' : 'pointer'
                    }}
                  >
                    <Plus size={15} />
                  </button>
                </div>
              </div>

              {/* Curated Add-ons */}
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Curated Upgrades & Add-ons
              </label>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {AVAILABLE_ADDONS.map(addon => {
                  const isChecked = selectedAddons.some(a => a.name === addon.name);
                  return (
                    <div
                      key={addon.id}
                      onClick={() => toggleAddon(addon)}
                      style={{
                        padding: '0.65rem 0.85rem',
                        borderRadius: 'var(--radius-md)',
                        border: isChecked ? '1px solid var(--primary)' : '1px solid var(--border-light)',
                        background: isChecked ? 'rgba(20, 184, 166, 0.08)' : 'var(--bg-card)',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        gap: '0.5rem',
                        transition: 'all var(--transition-fast)'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem' }}>
                        <span>{addon.icon}</span>
                        <span style={{ fontWeight: 600 }}>{addon.name}</span>
                      </div>
                      <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--primary)' }}>
                        +{formatPrice(addon.price)}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Right column: Traveller Contact Details */}
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Primary Traveller Information
              </label>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div>
                  <input
                    id="input-customer-name"
                    type="text"
                    required
                    placeholder="Full Legal Name"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 0.85rem',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card)',
                      fontSize: '0.9rem',
                      color: 'var(--text-main)',
                      outline: 'none'
                    }}
                  />
                </div>

                <div>
                  <input
                    id="input-customer-email"
                    type="email"
                    required
                    placeholder="Email Address (for ticket & itinerary)"
                    value={customerEmail}
                    onChange={(e) => setCustomerEmail(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 0.85rem',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card)',
                      fontSize: '0.9rem',
                      color: 'var(--text-main)',
                      outline: 'none'
                    }}
                  />
                </div>

                <div>
                  <input
                    id="input-customer-phone"
                    type="tel"
                    required
                    placeholder="Phone Number / WhatsApp"
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 0.85rem',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card)',
                      fontSize: '0.9rem',
                      color: 'var(--text-main)',
                      outline: 'none'
                    }}
                  />
                </div>

                <div>
                  <textarea
                    id="input-special-requests"
                    rows="3"
                    placeholder="Dietary requirements, anniversary notes, or room preferences..."
                    value={specialRequests}
                    onChange={(e) => setSpecialRequests(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '0.65rem 0.85rem',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-medium)',
                      background: 'var(--bg-card)',
                      fontSize: '0.85rem',
                      color: 'var(--text-main)',
                      outline: 'none'
                    }}
                  />
                </div>
              </div>

              {/* Price Calculation Box */}
              <div style={{
                marginTop: '1.25rem',
                padding: '1rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-card-subtle)',
                border: '1px solid var(--border-light)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.35rem', color: 'var(--text-secondary)' }}>
                  <span>{formatPrice(basePricePerPerson)} × {guestsCount} Guests</span>
                  <span>{formatPrice(basePricePerPerson * guestsCount)}</span>
                </div>
                {addonsTotalPerPerson > 0 && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.35rem', color: 'var(--text-secondary)' }}>
                    <span>Add-ons ({formatPrice(addonsTotalPerPerson)} × {guestsCount})</span>
                    <span>+{formatPrice(addonsTotalPerPerson * guestsCount)}</span>
                  </div>
                )}
                <div style={{
                  paddingTop: '0.5rem',
                  borderTop: '1px dashed var(--border-medium)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline'
                }}>
                  <strong style={{ fontSize: '0.95rem' }}>Total Reservation Amount</strong>
                  <span style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--primary)', fontFamily: 'var(--font-heading)' }}>
                    {formatPrice(grandTotal)}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Submit Actions */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            gap: '1rem',
            paddingTop: '1rem',
            borderTop: '1px solid var(--border-light)'
          }}>
            <button
              type="button"
              id="btn-cancel-booking"
              onClick={onClose}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              id="btn-confirm-booking-submit"
              disabled={submitting}
              className="btn-primary"
              style={{ padding: '0.75rem 2rem', fontWeight: 700 }}
            >
              <CreditCard size={18} />
              <span>{submitting ? 'Confirming Reservation...' : 'Confirm & Generate Ticket'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
