import React from 'react';
import { SlidersHorizontal, RotateCcw, Search, Sparkles, GraduationCap, Gem } from 'lucide-react';
import { useTravel } from '../context/TravelContext';

const CATEGORIES = ['All', 'Student', 'Luxury', 'Adventure', 'Cultural', 'Relaxation'];
const DIFFICULTIES = ['All', 'Easy', 'Moderate', 'Challenging'];

export default function FilterBar({
  filters,
  onFilterChange,
  onResetFilters,
  totalResults
}) {
  const { formatPrice } = useTravel();

  return (
    <div id="catalog-filter-bar" className="glass-panel" style={{
      borderRadius: 'var(--radius-lg)',
      padding: '1.25rem 1.5rem',
      marginBottom: '2rem'
    }}>
      {/* Category Pills Row with Student Special highlight */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '1rem',
        flexWrap: 'wrap',
        marginBottom: '1.25rem',
        paddingBottom: '1rem',
        borderBottom: '1px solid var(--border-light)'
      }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
          {CATEGORIES.map(cat => {
            const isActive = (filters.category === cat) || (!filters.category && cat === 'All');
            const isStudent = cat === 'Student';
            const isLuxury = cat === 'Luxury';

            return (
              <button
                key={cat}
                id={`filter-cat-${cat.toLowerCase()}`}
                onClick={() => onFilterChange('category', cat)}
                style={{
                  padding: '0.45rem 1.1rem',
                  borderRadius: 'var(--radius-full)',
                  border: isActive
                    ? '1.5px solid var(--primary)'
                    : isStudent
                      ? '1.5px dashed #0d9488'
                      : '1px solid var(--border-light)',
                  background: isActive
                    ? 'var(--primary)'
                    : isStudent
                      ? 'rgba(13, 148, 136, 0.08)'
                      : 'var(--bg-card)',
                  color: isActive
                    ? '#ffffff'
                    : isStudent
                      ? '#0f766e'
                      : 'var(--text-main)',
                  fontWeight: 700,
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.35rem',
                  transition: 'all var(--transition-fast)',
                  boxShadow: isActive ? '0 4px 12px var(--primary-glow)' : 'none'
                }}
              >
                {isStudent && <GraduationCap size={15} />}
                {isLuxury && <Gem size={14} />}
                <span>{isStudent ? 'Student & Budget (Under ₹3.5k)' : cat}</span>
              </button>
            );
          })}
        </div>

        {/* Total results & Reset */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            <strong>{totalResults}</strong> Trips Found
          </span>
          <button
            id="btn-reset-filters"
            onClick={onResetFilters}
            className="btn-secondary"
            style={{
              padding: '0.35rem 0.75rem',
              fontSize: '0.78rem',
              gap: '0.35rem'
            }}
          >
            <RotateCcw size={14} />
            <span>Reset</span>
          </button>
        </div>
      </div>

      {/* Advanced Filter Controls Row */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '1rem',
        alignItems: 'center'
      }}>
        {/* Search input */}
        <div>
          <label htmlFor="filter-search-input" style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.3rem' }}>
            Search Destination / Tour
          </label>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-md)',
            padding: '0.45rem 0.75rem',
            gap: '0.5rem'
          }}>
            <Search size={16} style={{ color: 'var(--text-muted)' }} />
            <input
              id="filter-search-input"
              type="text"
              placeholder="e.g. Shimla, Manali, Root Bridge..."
              value={filters.search || ''}
              onChange={(e) => onFilterChange('search', e.target.value)}
              style={{
                border: 'none',
                background: 'transparent',
                outline: 'none',
                width: '100%',
                fontSize: '0.85rem',
                color: 'var(--text-main)',
                fontWeight: 600
              }}
            />
          </div>
        </div>

        {/* Difficulty */}
        <div>
          <label htmlFor="filter-difficulty-select" style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.3rem' }}>
            Trip Pace
          </label>
          <select
            id="filter-difficulty-select"
            value={filters.difficulty || 'All'}
            onChange={(e) => onFilterChange('difficulty', e.target.value)}
            style={{
              width: '100%',
              padding: '0.55rem 0.75rem',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-medium)',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.85rem',
              fontWeight: 600,
              color: 'var(--text-main)',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            {DIFFICULTIES.map(d => (
              <option key={d} value={d}>{d === 'All' ? 'Any Pace' : d}</option>
            ))}
          </select>
        </div>

        {/* Max Price Slider (Supports Student Budget from $20 / ₹1,700 up to Luxury $3,000 / ₹2,50,000) */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Budget Filter
            </span>
            <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--primary)' }}>
              Up to {filters.max_price ? formatPrice(filters.max_price) : formatPrice(3000)}
            </span>
          </div>
          <input
            id="filter-price-slider"
            type="range"
            min="20"
            max="3000"
            step="20"
            value={filters.max_price || 3000}
            onChange={(e) => onFilterChange('max_price', e.target.value)}
            style={{
              width: '100%',
              accentColor: 'var(--primary)',
              cursor: 'pointer'
            }}
          />
        </div>

        {/* Sort selector */}
        <div>
          <label htmlFor="filter-sort-select" style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.3rem' }}>
            Sort By Price / Rating
          </label>
          <select
            id="filter-sort-select"
            value={filters.sort || 'featured'}
            onChange={(e) => onFilterChange('sort', e.target.value)}
            style={{
              width: '100%',
              padding: '0.55rem 0.75rem',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-medium)',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.85rem',
              fontWeight: 600,
              color: 'var(--text-main)',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            <option value="featured">Featured & Popular</option>
            <option value="price_low">Price: Lowest First (Budget & Student)</option>
            <option value="price_high">Price: Highest First (Ultra Luxury)</option>
            <option value="rating">Guest Rating: Highest</option>
            <option value="duration_short">Duration: Weekend / Short</option>
            <option value="duration_long">Duration: Extended Expeditions</option>
          </select>
        </div>
      </div>
    </div>
  );
}
