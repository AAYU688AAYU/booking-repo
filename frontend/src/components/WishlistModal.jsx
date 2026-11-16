import React from 'react';
import { X, Heart, Trash2, ArrowRight } from 'lucide-react';
import { useTravel } from '../context/TravelContext';

export default function WishlistModal({ tours, onClose, onOpenDetail, onBookNow }) {
  const { wishlist, toggleWishlist, formatPrice } = useTravel();

  const wishlistedTours = tours.filter(t => wishlist.includes(t.id));

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        id="wishlist-modal"
        className="modal-content animate-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '640px' }}
      >
        <div style={{
          padding: '1.25rem 1.75rem',
          borderBottom: '1px solid var(--border-light)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--bg-card-subtle)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Heart size={20} fill="#ef4444" color="#ef4444" />
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
              Saved Wishlist ({wishlistedTours.length})
            </h3>
          </div>
          <button
            id="btn-close-wishlist"
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

        <div style={{ padding: '1.5rem', maxHeight: '60vh', overflowY: 'auto' }}>
          {wishlistedTours.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-secondary)' }}>
              <Heart size={44} style={{ opacity: 0.25, marginBottom: '0.75rem', color: '#ef4444' }} />
              <h4 style={{ fontWeight: 700, marginBottom: '0.25rem' }}>Your Wishlist is Empty</h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                Click the heart icon on any expedition card to save it for your next adventure.
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {wishlistedTours.map(t => (
                <div
                  key={t.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1rem',
                    padding: '0.85rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-light)',
                    background: 'var(--bg-card)'
                  }}
                >
                  <img
                    src={t.image_url}
                    alt={t.title}
                    style={{
                      width: '80px',
                      height: '80px',
                      borderRadius: 'var(--radius-sm)',
                      objectFit: 'cover'
                    }}
                  />

                  <div style={{ flexGrow: 1, minWidth: 0 }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--primary)', fontWeight: 600 }}>
                      {t.destination_name}, {t.destination_country} • {t.duration_days} Days
                    </div>
                    <h4
                      onClick={() => {
                        onClose();
                        onOpenDetail(t.id);
                      }}
                      style={{
                        fontSize: '0.95rem',
                        fontWeight: 700,
                        lineHeight: 1.3,
                        cursor: 'pointer',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        marginBottom: '0.25rem'
                      }}
                    >
                      {t.title}
                    </h4>
                    <div style={{ fontWeight: 800, color: 'var(--text-main)', fontSize: '1rem', fontFamily: 'var(--font-heading)' }}>
                      {formatPrice(t.price_per_person)} <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>/person</span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', alignItems: 'flex-end' }}>
                    <button
                      id={`btn-book-wishlist-${t.id}`}
                      onClick={() => {
                        onClose();
                        onBookNow(t);
                      }}
                      className="btn-primary"
                      style={{ padding: '0.4rem 0.8rem', fontSize: '0.78rem', gap: '0.25rem' }}
                    >
                      <span>Book</span>
                      <ArrowRight size={12} />
                    </button>
                    <button
                      id={`btn-remove-wishlist-${t.id}`}
                      onClick={() => toggleWishlist(t.id)}
                      aria-label="Remove from wishlist"
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: 'var(--text-muted)',
                        padding: '0.2rem'
                      }}
                      title="Remove"
                    >
                      <Trash2 size={16} />
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
