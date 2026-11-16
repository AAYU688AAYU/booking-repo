import React, { useState } from 'react';
import { Compass, Mail, ShieldCheck, Award, Heart, CheckCircle2 } from 'lucide-react';

export default function Footer({ onNavigateSection }) {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer style={{
      background: 'var(--bg-card)',
      borderTop: '1px solid var(--border-light)',
      marginTop: '5rem',
      padding: '4rem 0 2rem 0'
    }}>
      <div className="container">
        {/* Top Newsletter Card */}
        <div className="glass-panel" style={{
          borderRadius: 'var(--radius-xl)',
          padding: '2.5rem',
          marginBottom: '3.5rem',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '2rem',
          alignItems: 'center',
          background: 'linear-gradient(135deg, rgba(20, 184, 166, 0.08) 0%, rgba(99, 102, 241, 0.06) 100%)'
        }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              The Private Dispatch
            </span>
            <h3 style={{ fontSize: '1.65rem', fontWeight: 800, marginTop: '0.25rem', marginBottom: '0.5rem' }}>
              Secret Itineraries In Your Inbox
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Receive invitations to rare seasonal departures, private yacht berths, and early-bird culinary masterclasses.
            </p>
          </div>

          <div>
            {subscribed ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontWeight: 600 }}>
                <CheckCircle2 size={20} />
                <span>You are subscribed to the bookwithgulshan Dispatch!</span>
              </div>
            ) : (
              <form onSubmit={handleSubscribe} style={{ display: 'flex', gap: '0.5rem' }}>
                <input
                  id="newsletter-email-input"
                  type="email"
                  required
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  style={{
                    flexGrow: 1,
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-medium)',
                    background: 'var(--bg-card)',
                    fontSize: '0.9rem',
                    outline: 'none',
                    color: 'var(--text-main)'
                  }}
                />
                <button
                  id="btn-newsletter-subscribe"
                  type="submit"
                  className="btn-primary"
                  style={{ padding: '0.75rem 1.5rem', flexShrink: 0 }}
                >
                  Join
                </button>
              </form>
            )}
          </div>
        </div>

        {/* Links Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '2.5rem',
          marginBottom: '3rem'
        }}>
          {/* Brand */}
          <div style={{ maxWidth: '320px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                background: 'var(--primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#fff'
              }}>
                <Compass size={20} />
              </div>
              <span style={{ fontSize: '1.35rem', fontWeight: 800 }}>bookwith<span style={{ color: 'var(--primary)' }}>gulshan</span></span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.6, marginBottom: '1rem' }}>
              Crafting once-in-a-lifetime journeys for discerning explorers. Certified carbon-neutral expeditions operated in harmony with local communities.
            </p>
            <div style={{ display: 'flex', gap: '0.75rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
              <span>★ 4.98/5 Rating</span>
              <span>•</span>
              <span>100% Guaranteed</span>
            </div>
          </div>

          {/* Expeditions */}
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '1rem' }}>Expeditions</h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              <li><a href="#catalog" onClick={() => onNavigateSection('catalog')}>Mediterranean Coastal Yachting</a></li>
              <li><a href="#catalog" onClick={() => onNavigateSection('catalog')}>Kyoto & Japan Heritage</a></li>
              <li><a href="#catalog" onClick={() => onNavigateSection('catalog')}>Swiss Alpine Glacier Treks</a></li>
              <li><a href="#catalog" onClick={() => onNavigateSection('catalog')}>Serengeti Great Migration</a></li>
              <li><a href="#catalog" onClick={() => onNavigateSection('catalog')}>Patagonia End-of-Earth</a></li>
            </ul>
          </div>

          {/* Destinations */}
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '1rem' }}>Destinations</h4>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
              <li><a href="#destinations" onClick={() => onNavigateSection('destinations')}>Italy & Amalfi</a></li>
              <li><a href="#destinations" onClick={() => onNavigateSection('destinations')}>Japan & Mount Fuji</a></li>
              <li><a href="#destinations" onClick={() => onNavigateSection('destinations')}>Switzerland & Zermatt</a></li>
              <li><a href="#destinations" onClick={() => onNavigateSection('destinations')}>Tanzania Savannahs</a></li>
              <li><a href="#destinations" onClick={() => onNavigateSection('destinations')}>Greece & Cyclades</a></li>
            </ul>
          </div>

          {/* Trust & Accreditations */}
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, marginBottom: '1rem' }}>Our Promise</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <ShieldCheck size={18} style={{ color: 'var(--primary)' }} />
                <span>Financial Bonded Protection</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <Award size={18} style={{ color: 'var(--accent)' }} />
                <span>Certified National Guides</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <Heart size={18} style={{ color: '#ef4444' }} />
                <span>1% for Planet Earth Conservation</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div style={{
          borderTop: '1px solid var(--border-light)',
          paddingTop: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '1rem',
          fontSize: '0.8rem',
          color: 'var(--text-muted)'
        }}>
          <div>
            © {new Date().getFullYear()} bookwithgulshan Luxury Expeditions Inc. Powered by Django REST Framework & React.
          </div>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <span>Privacy Policy</span>
            <span>Terms of Service</span>
            <span>Sustainable Travel Charter</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
