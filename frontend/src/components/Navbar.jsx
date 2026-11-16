import React from 'react';
import { Compass, Moon, Sun, Heart, Ticket, Globe, Sparkles } from 'lucide-react';
import { useTravel } from '../context/TravelContext';

export default function Navbar({ onOpenMyBookings, onOpenWishlist, onNavigateSection }) {
  const { theme, toggleTheme, currency, setCurrency, currencies, wishlist } = useTravel();

  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      width: '100%',
      background: 'var(--bg-glass-strong)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-light)',
      boxShadow: '0 4px 20px -5px rgba(0, 0, 0, 0.04)',
      transition: 'all var(--transition-normal)'
    }}>
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.9rem 1.5rem',
        gap: '1.5rem'
      }}>
        {/* Brand Logo */}
        <div
          id="nav-logo"
          onClick={() => onNavigateSection('hero')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.8rem',
            cursor: 'pointer',
            userSelect: 'none'
          }}
        >
          {/* Glowing Compass Badge */}
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: '13px',
            background: 'linear-gradient(135deg, #0f766e 0%, #14b8a6 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            boxShadow: '0 4px 16px rgba(20, 184, 166, 0.35)',
            border: '1px solid rgba(255, 255, 255, 0.3)',
            transition: 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)'
          }}
          onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.08) rotate(12deg)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1) rotate(0deg)'; }}
          >
            <Compass size={22} strokeWidth={2} />
          </div>

          <div>
            <div style={{
              fontFamily: 'var(--font-heading)',
              fontSize: '1.42rem',
              fontWeight: 800,
              letterSpacing: '-0.02em',
              lineHeight: 1.1,
              display: 'flex',
              alignItems: 'center',
              gap: '0.1rem'
            }}>
              <span style={{ color: 'var(--text-main)' }}>bookwith</span>
              <span style={{
                background: 'linear-gradient(135deg, var(--primary) 0%, #14b8a6 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 800
              }}>
                gulshan
              </span>
            </div>
            <div style={{
              fontSize: '0.66rem',
              fontWeight: 700,
              letterSpacing: '0.2em',
              textTransform: 'uppercase',
              color: 'var(--text-muted)',
              marginTop: '2px'
            }}>
              Luxury Expeditions
            </div>
          </div>
        </div>

        {/* Navigation links with stylish animated underline effects */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2.5rem',
        }} className="desktop-nav">
          <button
            id="nav-link-explore"
            className="nav-link-stylish"
            onClick={() => onNavigateSection('catalog')}
          >
            Explore Tours
          </button>

          <button
            id="nav-link-destinations"
            className="nav-link-stylish"
            onClick={() => onNavigateSection('destinations')}
          >
            Destinations
          </button>

          <button
            id="nav-link-reviews"
            className="nav-link-stylish"
            onClick={() => onNavigateSection('reviews')}
          >
            Traveller Stories
          </button>
        </nav>

        {/* Right utility buttons with enhanced button format and micro-interactions */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          {/* Stylish Currency Selector Pill */}
          <div className="nav-pill-currency">
            <Globe size={15} style={{ color: 'var(--primary)' }} />
            <select
              id="currency-selector"
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              style={{
                border: 'none',
                background: 'transparent',
                color: 'var(--text-main)',
                fontSize: '0.82rem',
                fontWeight: 700,
                letterSpacing: '0.02em',
                cursor: 'pointer',
                outline: 'none',
                paddingRight: '0.2rem'
              }}
            >
              {Object.keys(currencies).map(c => (
                <option key={c} value={c} style={{ background: 'var(--bg-card)', color: 'var(--text-main)' }}>
                  {currencies[c].label}
                </option>
              ))}
            </select>
          </div>

          {/* Wishlist Button with pulse counter */}
          <button
            id="nav-btn-wishlist"
            className="nav-icon-btn"
            onClick={onOpenWishlist}
            aria-label="View Saved Trips"
            style={{ position: 'relative' }}
          >
            <Heart
              size={18}
              strokeWidth={2}
              fill={wishlist.length > 0 ? '#ef4444' : 'none'}
              style={{ color: wishlist.length > 0 ? '#ef4444' : 'var(--text-secondary)' }}
            />
            {wishlist.length > 0 && (
              <span style={{
                position: 'absolute',
                top: '-4px',
                right: '-4px',
                background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                color: '#ffffff',
                fontSize: '0.64rem',
                fontWeight: 800,
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px rgba(239, 68, 68, 0.45)'
              }}>
                {wishlist.length}
              </span>
            )}
          </button>

          {/* My Bookings Button with gradient border & hover lift */}
          <button
            id="nav-btn-my-bookings"
            className="nav-btn-bookings"
            onClick={onOpenMyBookings}
          >
            <Ticket size={16} strokeWidth={2.2} />
            <span>My Bookings</span>
          </button>

          {/* Theme Toggle Button */}
          <button
            id="nav-btn-theme-toggle"
            className="nav-icon-btn"
            onClick={toggleTheme}
            aria-label="Toggle Theme"
          >
            {theme === 'light' ? (
              <Moon size={17} strokeWidth={2} />
            ) : (
              <Sun size={17} strokeWidth={2} style={{ color: '#fbbf24' }} />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
