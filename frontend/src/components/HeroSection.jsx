import React, { useState } from 'react';
import { Search, MapPin, Calendar, Users, Compass, ArrowRight, ShieldCheck, Star } from 'lucide-react';

export default function HeroSection({ destinations, onSearchSubmit, stats }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDestination, setSelectedDestination] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedSeason, setSelectedSeason] = useState('');
  const [activeTab, setActiveTab] = useState('all');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearchSubmit({
      search: searchTerm,
      destination: selectedDestination,
      category: selectedCategory === 'All' ? '' : selectedCategory,
    });
  };

  const handleQuickTagClick = (destName, cat) => {
    let destId = '';
    if (destName) {
      const match = destinations.find(d => d.name.toLowerCase().includes(destName.toLowerCase()));
      if (match) destId = String(match.id);
    }
    setSelectedDestination(destId);
    setSelectedCategory(cat || '');
    onSearchSubmit({
      search: '',
      destination: destId,
      category: cat || '',
    });
  };

  return (
    <section
      id="hero-section"
      style={{
        position: 'relative',
        minHeight: '82vh',
        display: 'flex',
        alignItems: 'center',
        padding: '5rem 0 4rem 0',
        overflow: 'hidden',
        color: '#ffffff'
      }}
    >
      {/* High-Resolution Cinematic Background Image */}
      <div style={{
        position: 'absolute',
        inset: 0,
        zIndex: 1,
        overflow: 'hidden'
      }}>
        <img
          src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=2400&q=85"
          alt="Luxury Destination"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: 'center 40%',
            filter: 'brightness(0.85) contrast(1.05)'
          }}
        />
        {/* Layered Editorial Gradient Overlays */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(180deg, rgba(10, 17, 28, 0.72) 0%, rgba(10, 17, 28, 0.45) 50%, rgba(10, 17, 28, 0.88) 100%)'
        }} />
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(ellipse at 50% 30%, transparent 40%, rgba(8, 14, 24, 0.6) 100%)'
        }} />
      </div>

      <div className="container" style={{ position: 'relative', zIndex: 2, width: '100%' }}>
        {/* Editorial Subtitle Label */}
        <div style={{ textAlign: 'center', marginBottom: '1.25rem' }}>
          <span style={{
            display: 'inline-block',
            fontSize: '0.76rem',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.22em',
            color: '#e2e8f0',
            borderBottom: '1px solid rgba(255, 255, 255, 0.35)',
            paddingBottom: '0.35rem'
          }}>
            PRIVATE EXPEDITIONS & BESPOKE SANCTUARIES
          </span>
        </div>

        {/* Sophisticated Editorial Headline */}
        <div style={{ textAlign: 'center', maxWidth: '920px', margin: '0 auto 2rem auto' }}>
          <h1 style={{
            fontSize: 'clamp(2.4rem, 5.2vw, 4.4rem)',
            fontWeight: 700,
            letterSpacing: '-0.025em',
            lineHeight: 1.15,
            color: '#ffffff',
            marginBottom: '1.25rem',
            textShadow: '0 2px 20px rgba(0,0,0,0.4)'
          }}>
            Extraordinary Journeys Across <br />
            <span style={{
              fontFamily: 'var(--font-serif)',
              fontStyle: 'italic',
              fontWeight: 400,
              color: '#fef08a'
            }}>
              The World's Most Evocative
            </span> Sanctuaries.
          </h1>

          <p style={{
            fontSize: 'clamp(1rem, 1.3vw, 1.2rem)',
            color: 'rgba(255, 255, 255, 0.86)',
            lineHeight: 1.6,
            maxWidth: '680px',
            margin: '0 auto',
            fontWeight: 400
          }}>
            Hand-crafted private and small-group voyages curated by cultural historians,
            master wildlife trackers, and regional connoisseurs.
          </p>
        </div>

        {/* Student Special Callout Pill */}
        <div style={{ textAlign: 'center', marginBottom: '1.25rem' }}>
          <button
            type="button"
            onClick={() => handleQuickTagClick('Shimla', 'Student')}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.6rem',
              background: 'rgba(234, 179, 8, 0.18)',
              border: '1px solid rgba(234, 179, 8, 0.55)',
              color: '#fef08a',
              padding: '0.45rem 1.1rem',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.84rem',
              fontWeight: 600,
              cursor: 'pointer',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 4px 15px rgba(0,0,0,0.25)',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.03)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
          >
            <span style={{ fontSize: '1rem' }}>🎓</span>
            <span><strong>Student Special:</strong> Explore <strong>Shimla for ₹2,000</strong> & Manali in ₹3,200 with complete transit guides</span>
            <ArrowRight size={14} />
          </button>
        </div>

        {/* Luxury Booking & Search Console */}
        <div style={{ maxWidth: '1020px', margin: '0 auto' }}>
          {/* Subtle Category Segmented Tabs */}
          <div style={{
            display: 'flex',
            gap: '0.5rem',
            marginBottom: '0.6rem',
            paddingLeft: '0.5rem',
            overflowX: 'auto',
            paddingBottom: '2px'
          }}>
            {[
              { id: 'all', label: 'All Expeditions', cat: '' },
              { id: 'student', label: '🎓 Student Deals (From ₹2k)', cat: 'Student' },
              { id: 'luxury', label: '💎 Ultra-Luxury Sanctuaries', cat: 'Luxury' },
              { id: 'adventure', label: '🏔️ Mountain & Adventure', cat: 'Adventure' },
              { id: 'cultural', label: '🏛️ Cultural & Heritage', cat: 'Cultural' },
            ].map(tab => {
              const isSelected = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => {
                    setActiveTab(tab.id);
                    setSelectedCategory(tab.cat);
                    onSearchSubmit({
                      search: searchTerm,
                      destination: selectedDestination,
                      category: tab.cat
                    });
                  }}
                  style={{
                    background: isSelected ? 'rgba(255, 255, 255, 0.95)' : 'rgba(15, 23, 42, 0.65)',
                    color: isSelected ? '#0f172a' : 'rgba(255, 255, 255, 0.85)',
                    backdropFilter: 'blur(8px)',
                    border: isSelected ? '1px solid #ffffff' : '1px solid rgba(255, 255, 255, 0.2)',
                    padding: '0.45rem 1.1rem',
                    borderRadius: 'var(--radius-md) var(--radius-md) 0 0',
                    fontSize: '0.82rem',
                    fontWeight: 600,
                    letterSpacing: '0.02em',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap',
                    transition: 'all var(--transition-fast)'
                  }}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>

          {/* Segmented Search Console Bar */}
          <form
            id="hero-search-form"
            onSubmit={handleSearch}
            style={{
              background: 'rgba(255, 255, 255, 0.96)',
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
              borderRadius: 'var(--radius-lg)',
              padding: '0.75rem 1rem',
              display: 'grid',
              gridTemplateColumns: '1.2fr 1fr 1fr 1fr auto',
              gap: '0.75rem',
              alignItems: 'center',
              boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.1)',
              color: '#0f172a'
            }}
          >
            {/* Segment 1: Destination */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem',
              padding: '0.45rem 0.75rem'
            }}>
              <MapPin size={18} style={{ color: 'var(--primary)', flexShrink: 0 }} />
              <div style={{ width: '100%' }}>
                <label
                  htmlFor="destination-select"
                  style={{
                    display: 'block',
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                    color: '#64748b',
                    marginBottom: '2px'
                  }}
                >
                  Destination
                </label>
                <select
                  id="destination-select"
                  value={selectedDestination}
                  onChange={(e) => setSelectedDestination(e.target.value)}
                  style={{
                    width: '100%',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.92rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    outline: 'none',
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  <option value="">Any Region / Country</option>
                  {destinations.map(d => (
                    <option key={d.id} value={d.id}>
                      {d.name}, {d.country}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Segment 2: Travel Season */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem',
              padding: '0.45rem 0.75rem',
              borderLeft: '1px solid #e2e8f0'
            }}>
              <Calendar size={18} style={{ color: 'var(--accent)', flexShrink: 0 }} />
              <div style={{ width: '100%' }}>
                <label
                  htmlFor="season-select"
                  style={{
                    display: 'block',
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                    color: '#64748b',
                    marginBottom: '2px'
                  }}
                >
                  Travel Window
                </label>
                <select
                  id="season-select"
                  value={selectedSeason}
                  onChange={(e) => setSelectedSeason(e.target.value)}
                  style={{
                    width: '100%',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.92rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    outline: 'none',
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  <option value="">Flexible Dates</option>
                  <option value="spring">Spring (Apr - Jun)</option>
                  <option value="summer">Summer (Jul - Aug)</option>
                  <option value="autumn">Autumn (Sep - Nov)</option>
                  <option value="winter">Winter (Dec - Mar)</option>
                </select>
              </div>
            </div>

            {/* Segment 3: Experience Style */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem',
              padding: '0.45rem 0.75rem',
              borderLeft: '1px solid #e2e8f0'
            }}>
              <Compass size={18} style={{ color: 'var(--primary)', flexShrink: 0 }} />
              <div style={{ width: '100%' }}>
                <label
                  htmlFor="category-select"
                  style={{
                    display: 'block',
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                    color: '#64748b',
                    marginBottom: '2px'
                  }}
                >
                  Experience Style
                </label>
                <select
                  id="category-select"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  style={{
                    width: '100%',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.92rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    outline: 'none',
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  <option value="">All Styles (Budget & Luxury)</option>
                  <option value="Student">🎓 Student Backpacker (Under ₹2,000 - ₹3.5k)</option>
                  <option value="Budget">💰 Budget & Weekend Escapes</option>
                  <option value="Luxury">💎 Ultra-Luxury & 5-Star Sanctuaries</option>
                  <option value="Adventure">🏔️ Mountain Treks & Adventure</option>
                  <option value="Cultural">🏛️ Cultural & Heritage</option>
                  <option value="Wildlife">🦁 Safari & Wildlife</option>
                  <option value="Relaxation">🌊 Coastal & Wellness</option>
                </select>
              </div>
            </div>

            {/* Segment 4: Search keyword */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.65rem',
              padding: '0.45rem 0.75rem',
              borderLeft: '1px solid #e2e8f0'
            }}>
              <Search size={18} style={{ color: '#94a3b8', flexShrink: 0 }} />
              <div style={{ width: '100%' }}>
                <label
                  htmlFor="search-input"
                  style={{
                    display: 'block',
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: '0.08em',
                    color: '#64748b',
                    marginBottom: '2px'
                  }}
                >
                  Search Keyword
                </label>
                <input
                  id="search-input"
                  type="text"
                  placeholder="e.g. Shimla 2k, Manali, Camp, Luxury"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  style={{
                    width: '100%',
                    border: 'none',
                    background: 'transparent',
                    fontSize: '0.92rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    outline: 'none'
                  }}
                />
              </div>
            </div>

            {/* Submit Action Button */}
            <button
              id="btn-hero-search"
              type="submit"
              style={{
                height: '48px',
                padding: '0 1.6rem',
                borderRadius: 'var(--radius-md)',
                background: 'linear-gradient(135deg, #0f766e 0%, #115e59 100%)',
                color: '#ffffff',
                border: 'none',
                fontWeight: 600,
                fontSize: '0.9rem',
                letterSpacing: '0.02em',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                boxShadow: '0 4px 14px rgba(15, 118, 110, 0.4)',
                transition: 'all var(--transition-fast)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-1px)';
                e.currentTarget.style.boxShadow = '0 6px 18px rgba(15, 118, 110, 0.55)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 14px rgba(15, 118, 110, 0.4)';
              }}
            >
              <span>Explore</span>
              <ArrowRight size={15} />
            </button>
          </form>

          {/* Trending Destinations Quick Links */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.65rem',
            marginTop: '1.25rem',
            fontSize: '0.82rem',
            color: 'rgba(255, 255, 255, 0.78)',
            flexWrap: 'wrap'
          }}>
            <span style={{ fontWeight: 600, color: 'rgba(255, 255, 255, 0.95)' }}>Trending Deals & Destinations:</span>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Shimla', 'Student')}
              style={{
                background: 'rgba(234, 179, 8, 0.28)',
                border: '1px solid rgba(254, 240, 138, 0.7)',
                color: '#fef08a',
                padding: '0.25rem 0.8rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.8rem',
                fontWeight: 700,
                cursor: 'pointer',
                boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
              }}
            >
              🎓 Shimla (₹2,000 Deal)
            </button>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Manali', '')}
              style={{
                background: 'rgba(255, 255, 255, 0.16)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: '#ffffff',
                padding: '0.2rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                cursor: 'pointer'
              }}
            >
              Manali (₹3.2k Camp / ₹1.2L Heli)
            </button>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Meghalaya', '')}
              style={{
                background: 'rgba(255, 255, 255, 0.16)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: '#ffffff',
                padding: '0.2rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                cursor: 'pointer'
              }}
            >
              Meghalaya (Root Bridges & Dawki)
            </button>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Amalfi', 'Luxury')}
              style={{
                background: 'rgba(255, 255, 255, 0.16)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: '#ffffff',
                padding: '0.2rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                cursor: 'pointer'
              }}
            >
              Amalfi Coast & Capri
            </button>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Kyoto', 'Cultural')}
              style={{
                background: 'rgba(255, 255, 255, 0.16)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: '#ffffff',
                padding: '0.2rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                cursor: 'pointer'
              }}
            >
              Kyoto Temples
            </button>
            <button
              type="button"
              onClick={() => handleQuickTagClick('Swiss', 'Adventure')}
              style={{
                background: 'rgba(255, 255, 255, 0.16)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                color: '#ffffff',
                padding: '0.2rem 0.75rem',
                borderRadius: 'var(--radius-full)',
                fontSize: '0.78rem',
                cursor: 'pointer'
              }}
            >
              Swiss Alpine
            </button>
          </div>
        </div>

        {/* Editorial Press & Recognition Strip */}
        <div style={{
          marginTop: '3.5rem',
          paddingTop: '1.75rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1.5rem',
          color: 'rgba(255, 255, 255, 0.7)'
        }}>
          <div style={{ fontSize: '0.72rem', letterSpacing: '0.15em', textTransform: 'uppercase', fontWeight: 600 }}>
            Featured In Premier Publications
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '2.5rem',
            fontSize: '0.85rem',
            fontFamily: 'var(--font-serif)',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            opacity: 0.85,
            flexWrap: 'wrap'
          }}>
            <span>Condé Nast Traveler</span>
            <span>Financial Times</span>
            <span>Travel + Leisure</span>
            <span>Robb Report</span>
          </div>
        </div>
      </div>
    </section>
  );
}
