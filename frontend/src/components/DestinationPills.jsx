import React from 'react';
import { MapPin, Sun, CloudRain } from 'lucide-react';

export default function DestinationPills({ destinations, activeDestinationId, onSelectDestination }) {
  return (
    <section id="destinations" style={{ padding: '2.5rem 0 1.5rem 0' }}>
      <div className="container">
        <div style={{
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'space-between',
          marginBottom: '1.5rem',
          flexWrap: 'wrap',
          gap: '1rem'
        }}>
          <div>
            <div style={{
              fontSize: '0.8rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
              color: 'var(--primary)',
              marginBottom: '0.25rem'
            }}>
              Curated Escapes
            </div>
            <h2 style={{ fontSize: '1.85rem', fontWeight: 800 }}>
              Explore By Destination
            </h2>
          </div>

          {activeDestinationId && (
            <button
              id="btn-clear-destination"
              onClick={() => onSelectDestination(null)}
              className="btn-secondary"
              style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }}
            >
              Show All Destinations
            </button>
          )}
        </div>

        {/* Destination Scroll/Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
          gap: '1rem'
        }}>
          {destinations.map(d => {
            const isActive = activeDestinationId === d.id;
            return (
              <div
                key={d.id}
                id={`destination-card-${d.id}`}
                onClick={() => onSelectDestination(isActive ? null : d.id)}
                style={{
                  position: 'relative',
                  height: '160px',
                  borderRadius: 'var(--radius-lg)',
                  overflow: 'hidden',
                  cursor: 'pointer',
                  border: isActive ? '2px solid var(--primary)' : '1px solid var(--border-light)',
                  boxShadow: isActive ? '0 8px 24px var(--primary-glow)' : 'var(--shadow-sm)',
                  transition: 'all var(--transition-normal)',
                  transform: isActive ? 'scale(1.02)' : 'none'
                }}
              >
                <img
                  src={d.image_url}
                  alt={d.name}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'brightness(0.65)',
                    transition: 'transform 0.4s ease'
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.08)'; }}
                  onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
                />
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 60%, transparent 100%)',
                  padding: '1rem',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'flex-end',
                  color: '#ffffff'
                }}>
                  <div style={{
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    color: 'rgba(255,255,255,0.75)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em'
                  }}>
                    {d.country}
                  </div>
                  <div style={{
                    fontSize: '1.15rem',
                    fontWeight: 700,
                    lineHeight: 1.2,
                    marginBottom: '0.25rem'
                  }}>
                    {d.name}
                  </div>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: '0.75rem',
                    color: 'rgba(255,255,255,0.9)'
                  }}>
                    <span>{d.tour_count || 1} Expedition{d.tour_count > 1 ? 's' : ''}</span>
                    <span style={{
                      background: 'rgba(255,255,255,0.25)',
                      backdropFilter: 'blur(4px)',
                      padding: '0.15rem 0.5rem',
                      borderRadius: 'var(--radius-full)'
                    }}>
                      {d.region}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
