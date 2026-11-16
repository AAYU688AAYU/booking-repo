import React from 'react';
import { Heart, Star, Clock, MapPin, Users, CheckCircle2, ArrowRight, GraduationCap, Gem, Compass } from 'lucide-react';
import { useTravel } from '../context/TravelContext';

export default function TourCard({ tour, onOpenDetail, onBookNow }) {
  const { isWishlisted, toggleWishlist, formatPrice } = useTravel();
  const wishlisted = isWishlisted(tour.id);
  const isStudent = tour.category === 'Student';
  const isLuxury = tour.category === 'Luxury';

  return (
    <article
      id={`tour-card-${tour.id}`}
      style={{
        background: 'var(--bg-card)',
        borderRadius: 'var(--radius-xl)',
        overflow: 'hidden',
        border: isStudent ? '1.5px solid rgba(13, 148, 136, 0.35)' : '1px solid var(--border-light)',
        boxShadow: isStudent ? '0 4px 18px rgba(13, 148, 136, 0.1)' : 'var(--shadow-md)',
        display: 'flex',
        flexDirection: 'column',
        transition: 'all var(--transition-normal)',
        position: 'relative'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-6px)';
        e.currentTarget.style.boxShadow = 'var(--shadow-xl)';
        e.currentTarget.style.borderColor = 'var(--primary)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = isStudent ? '0 4px 18px rgba(13, 148, 136, 0.1)' : 'var(--shadow-md)';
        e.currentTarget.style.borderColor = isStudent ? 'rgba(13, 148, 136, 0.35)' : 'var(--border-light)';
      }}
    >
      {/* Tour Image Header */}
      <div style={{ position: 'relative', height: '230px', overflow: 'hidden' }}>
        <img
          src={tour.image_url}
          alt={tour.title}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'transform 0.5s ease'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.06)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
        />

        {/* Top Gradient Overlay */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, transparent 40%, rgba(0,0,0,0.7) 100%)'
        }} />

        {/* Badges top left */}
        <div style={{ position: 'absolute', top: '1rem', left: '1rem', display: 'flex', gap: '0.4rem', zIndex: 2, flexWrap: 'wrap' }}>
          {isStudent && (
            <span className="badge" style={{
              background: 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
              color: '#ffffff',
              boxShadow: '0 2px 8px rgba(5, 150, 105, 0.4)'
            }}>
              <GraduationCap size={13} style={{ marginRight: '3px' }} />
              Student Special
            </span>
          )}
          {isLuxury && (
            <span className="badge" style={{
              background: 'linear-gradient(135deg, #b45309 0%, #d97706 100%)',
              color: '#ffffff',
              boxShadow: '0 2px 8px rgba(180, 83, 9, 0.4)'
            }}>
              <Gem size={12} style={{ marginRight: '3px' }} />
              Ultra Luxury
            </span>
          )}
          {tour.is_featured && !isStudent && !isLuxury && (
            <span className="badge badge-featured">
              ★ Featured
            </span>
          )}
          <span className="badge" style={{
            background: 'rgba(15, 23, 42, 0.75)',
            color: '#ffffff',
            backdropFilter: 'blur(8px)'
          }}>
            {tour.category}
          </span>
        </div>

        {/* Wishlist button top right */}
        <button
          id={`btn-wishlist-${tour.id}`}
          onClick={(e) => {
            e.stopPropagation();
            toggleWishlist(tour.id);
          }}
          aria-label={wishlisted ? 'Remove from wishlist' : 'Save to wishlist'}
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.9)',
            border: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            zIndex: 3,
            color: wishlisted ? '#ef4444' : '#64748b',
            boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
            transition: 'transform var(--transition-fast)'
          }}
        >
          <Heart size={18} fill={wishlisted ? '#ef4444' : 'none'} />
        </button>

        {/* Location & Duration bottom */}
        <div style={{
          position: 'absolute',
          bottom: '0.75rem',
          left: '1rem',
          right: '1rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          color: '#ffffff',
          fontSize: '0.8rem',
          fontWeight: 600,
          zIndex: 2
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <MapPin size={15} style={{ color: '#2dd4bf' }} />
            <span>{tour.destination_name}, {tour.destination_country}</span>
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.35rem',
            background: 'rgba(0,0,0,0.45)',
            padding: '0.2rem 0.6rem',
            borderRadius: 'var(--radius-full)',
            backdropFilter: 'blur(4px)'
          }}>
            <Clock size={13} />
            <span>{tour.duration_days} Days / {tour.duration_days - 1} N</span>
          </div>
        </div>
      </div>

      {/* Card Body */}
      <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
        {/* Rating and group size */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '0.5rem',
          fontSize: '0.82rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <Star size={15} style={{ color: 'var(--accent)', fill: 'var(--accent)' }} />
            <strong style={{ color: 'var(--text-main)' }}>{tour.rating}</strong>
            <span style={{ color: 'var(--text-muted)' }}>({tour.review_count || 32} reviews)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: 'var(--text-secondary)' }}>
            <Users size={14} />
            <span>Max {tour.group_size_max || 10} travelers</span>
          </div>
        </div>

        {/* Title */}
        <h3
          onClick={() => onOpenDetail(tour.id)}
          style={{
            fontSize: '1.18rem',
            fontWeight: 700,
            lineHeight: 1.35,
            marginBottom: '0.5rem',
            cursor: 'pointer',
            transition: 'color var(--transition-fast)'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--primary)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-main)'; }}
        >
          {tour.title}
        </h3>

        {/* Transit Time Duration Banner (Crucial for Travel Planning) */}
        {tour.travel_time && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.4rem 0.65rem',
            background: isStudent ? 'rgba(5, 150, 105, 0.08)' : 'rgba(15, 118, 110, 0.06)',
            border: isStudent ? '1px solid rgba(5, 150, 105, 0.25)' : '1px dashed var(--border-medium)',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.78rem',
            color: isStudent ? '#047857' : 'var(--primary)',
            fontWeight: 600,
            marginBottom: '0.75rem'
          }}>
            <Clock size={13} style={{ flexShrink: 0 }} />
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              <strong>Transit:</strong> {tour.travel_time}
            </span>
          </div>
        )}

        {/* Short description */}
        <p style={{
          fontSize: '0.86rem',
          color: 'var(--text-secondary)',
          lineHeight: 1.5,
          marginBottom: '0.85rem',
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden'
        }}>
          {tour.short_description}
        </p>

        {/* Key Highlights preview */}
        {tour.highlights && tour.highlights.length > 0 && (
          <div style={{ marginBottom: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
            {tour.highlights.slice(0, 2).map((h, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.45rem', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                <CheckCircle2 size={14} style={{ color: 'var(--primary)', flexShrink: 0, marginTop: '2px' }} />
                <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{h}</span>
              </div>
            ))}
          </div>
        )}

        {/* Price & Action Buttons */}
        <div style={{
          marginTop: 'auto',
          paddingTop: '1rem',
          borderTop: '1px solid var(--border-light)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '0.75rem'
        }}>
          <div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
              {isStudent ? '🎓 Student Price' : 'From'}
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.35rem' }}>
              <span style={{
                fontSize: '1.4rem',
                fontWeight: 800,
                color: isStudent ? '#047857' : 'var(--text-main)',
                fontFamily: 'var(--font-heading)'
              }}>
                {formatPrice(tour.price_per_person)}
              </span>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>/person</span>
            </div>
            {tour.original_price && (
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textDecoration: 'line-through' }}>
                {formatPrice(tour.original_price)}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '0.4rem' }}>
            <button
              id={`btn-tour-detail-${tour.id}`}
              onClick={() => onOpenDetail(tour.id)}
              className="btn-secondary"
              style={{ padding: '0.55rem 0.85rem', fontSize: '0.85rem' }}
            >
              Itinerary
            </button>
            <button
              id={`btn-tour-book-${tour.id}`}
              onClick={() => onBookNow(tour)}
              className="btn-primary"
              style={{
                padding: '0.55rem 1rem',
                fontSize: '0.85rem',
                gap: '0.3rem',
                background: isStudent ? 'linear-gradient(135deg, #059669 0%, #047857 100%)' : undefined
              }}
            >
              <span>Book</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}
