import React, { useState, useEffect } from 'react';
import {
  X, Star, Clock, MapPin, Users, Check, AlertCircle,
  Calendar, ChevronDown, ChevronUp, MessageSquare, Send, Heart
} from 'lucide-react';
import { useTravel } from '../context/TravelContext';
import { api } from '../services/api';

export default function TourDetailModal({ tourId, onClose, onBookTour }) {
  const { formatPrice, isWishlisted, toggleWishlist } = useTravel();
  const [tour, setTour] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeImage, setActiveImage] = useState('');
  const [expandedDay, setExpandedDay] = useState(1);

  // Review form state
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [reviewName, setReviewName] = useState('');
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewTitle, setReviewTitle] = useState('');
  const [reviewComment, setReviewComment] = useState('');
  const [reviewTravelType, setReviewTravelType] = useState('Couple');
  const [reviewSubmitting, setReviewSubmitting] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  useEffect(() => {
    if (!tourId) return;
    setLoading(true);
    api.getTripDetail(tourId)
      .then(data => {
        setTour(data);
        setActiveImage(data.image_url);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [tourId]);

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    if (!reviewName || !reviewTitle || !reviewComment) return;

    setReviewSubmitting(true);
    try {
      const newReview = await api.addReview(tour.id, {
        author_name: reviewName,
        rating: reviewRating,
        title: reviewTitle,
        comment: reviewComment,
        travel_type: reviewTravelType,
      });

      // Update state with new review
      setTour(prev => ({
        ...prev,
        reviews: [newReview, ...(prev.reviews || [])],
        review_count: (prev.review_count || 0) + 1,
      }));
      setReviewSuccess(true);
      setShowReviewForm(false);
      // Reset form
      setReviewName('');
      setReviewTitle('');
      setReviewComment('');
    } catch (err) {
      alert(err.message || 'Error submitting review');
    } finally {
      setReviewSubmitting(false);
    }
  };

  if (!tourId) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        id="tour-detail-modal"
        className="modal-content animate-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{ maxWidth: '900px', maxHeight: '92vh', overflowY: 'auto' }}
      >
        {/* Close Button */}
        <button
          id="btn-close-detail-modal"
          onClick={onClose}
          aria-label="Close Modal"
          style={{
            position: 'absolute',
            top: '1.25rem',
            right: '1.25rem',
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            background: 'rgba(0,0,0,0.6)',
            color: '#ffffff',
            border: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            zIndex: 10,
            backdropFilter: 'blur(4px)'
          }}
        >
          <X size={20} />
        </button>

        {loading ? (
          <div style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            <div className="animate-spin-slow" style={{ fontSize: '2rem', marginBottom: '1rem' }}>🧭</div>
            <p>Gathering expedition details...</p>
          </div>
        ) : error || !tour ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#ef4444' }}>
            <AlertCircle size={32} style={{ marginBottom: '0.5rem' }} />
            <p>{error || 'Could not load tour details.'}</p>
          </div>
        ) : (
          <div>
            {/* Gallery Header */}
            <div style={{ position: 'relative' }}>
              <div style={{ height: '380px', overflow: 'hidden' }}>
                <img
                  src={activeImage}
                  alt={tour.title}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>

              {/* Badges Overlay */}
              <div style={{
                position: 'absolute',
                bottom: '1rem',
                left: '1.5rem',
                display: 'flex',
                gap: '0.5rem',
                flexWrap: 'wrap'
              }}>
                <span className="badge badge-featured">{tour.category}</span>
                <span className="badge" style={{ background: 'rgba(0,0,0,0.7)', color: '#fff', backdropFilter: 'blur(6px)' }}>
                  <Clock size={13} style={{ marginRight: '4px' }} />
                  {tour.duration_days} Days / {tour.duration_days - 1} Nights
                </span>
                <span className="badge" style={{ background: 'rgba(0,0,0,0.7)', color: '#fff', backdropFilter: 'blur(6px)' }}>
                  <Users size={13} style={{ marginRight: '4px' }} />
                  Max {tour.group_size_max} Guests
                </span>
              </div>
            </div>

            {/* Gallery Thumbnails */}
            {tour.gallery_urls && tour.gallery_urls.length > 0 && (
              <div style={{
                display: 'flex',
                gap: '0.6rem',
                padding: '0.75rem 1.5rem',
                background: 'var(--bg-card-subtle)',
                overflowX: 'auto'
              }}>
                <div
                  onClick={() => setActiveImage(tour.image_url)}
                  style={{
                    width: '65px',
                    height: '50px',
                    borderRadius: 'var(--radius-sm)',
                    overflow: 'hidden',
                    cursor: 'pointer',
                    border: activeImage === tour.image_url ? '2px solid var(--primary)' : '1px solid transparent',
                    flexShrink: 0
                  }}
                >
                  <img src={tour.image_url} alt="Cover" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </div>
                {tour.gallery_urls.map((url, i) => (
                  <div
                    key={i}
                    onClick={() => setActiveImage(url)}
                    style={{
                      width: '65px',
                      height: '50px',
                      borderRadius: 'var(--radius-sm)',
                      overflow: 'hidden',
                      cursor: 'pointer',
                      border: activeImage === url ? '2px solid var(--primary)' : '1px solid transparent',
                      flexShrink: 0
                    }}
                  >
                    <img src={url} alt={`Gallery ${i}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  </div>
                ))}
              </div>
            )}

            {/* Content Body */}
            <div style={{ padding: '1.75rem' }}>
              {/* Destination & Title */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary)', fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.4rem' }}>
                <MapPin size={17} />
                <span>{tour.destination?.name}, {tour.destination?.country}</span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem', marginBottom: '1.25rem' }}>
                <h2 style={{ fontSize: '1.85rem', fontWeight: 800, lineHeight: 1.25 }}>
                  {tour.title}
                </h2>
                <button
                  id="btn-detail-wishlist"
                  onClick={() => toggleWishlist(tour.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.4rem',
                    padding: '0.5rem 0.9rem',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border-medium)',
                    background: 'var(--bg-card)',
                    color: isWishlisted(tour.id) ? '#ef4444' : 'var(--text-main)',
                    cursor: 'pointer',
                    flexShrink: 0
                  }}
                >
                  <Heart size={18} fill={isWishlisted(tour.id) ? '#ef4444' : 'none'} />
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                    {isWishlisted(tour.id) ? 'Saved' : 'Save'}
                  </span>
                </button>
              </div>

              {/* Ratings and overview */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1.5rem',
                padding: '0.9rem 1.25rem',
                borderRadius: 'var(--radius-md)',
                background: 'var(--bg-card-subtle)',
                marginBottom: '1rem',
                flexWrap: 'wrap'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <Star size={18} style={{ color: 'var(--accent)', fill: 'var(--accent)' }} />
                  <span style={{ fontSize: '1.1rem', fontWeight: 700 }}>{tour.rating}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    ({tour.review_count || 32} verified reviews)
                  </span>
                </div>
                <div style={{ height: '20px', width: '1px', background: 'var(--border-medium)' }} />
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Pace: <strong>{tour.difficulty}</strong>
                </div>
                {tour.category === 'Student' && (
                  <div style={{
                    marginLeft: 'auto',
                    background: 'rgba(5, 150, 105, 0.15)',
                    color: '#047857',
                    fontWeight: 700,
                    fontSize: '0.8rem',
                    padding: '0.25rem 0.65rem',
                    borderRadius: 'var(--radius-full)'
                  }}>
                    🎓 Student & Backpacker Budget Special
                  </div>
                )}
              </div>

              {/* Transit & Journey Duration info box */}
              {tour.travel_time && (
                <div style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.65rem',
                  padding: '0.85rem 1.15rem',
                  background: 'rgba(15, 118, 110, 0.07)',
                  border: '1px dashed rgba(15, 118, 110, 0.35)',
                  borderRadius: 'var(--radius-md)',
                  marginBottom: '1.5rem',
                  fontSize: '0.88rem',
                  color: 'var(--text-main)',
                  lineHeight: 1.45
                }}>
                  <Clock size={17} style={{ color: 'var(--primary)', flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <strong style={{ color: 'var(--primary)', display: 'block', marginBottom: '2px' }}>
                      Travel Duration & Transit Route:
                    </strong>
                    <span>{tour.travel_time}</span>
                  </div>
                </div>
              )}

              {/* Detailed Overview */}
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ fontSize: '1.25rem', marginBottom: '0.75rem', fontWeight: 700 }}>
                  Expedition Overview
                </h3>
                <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem' }}>
                  {tour.detailed_overview || tour.short_description}
                </p>
              </div>

              {/* Highlights List */}
              {tour.highlights && tour.highlights.length > 0 && (
                <div style={{ marginBottom: '2rem' }}>
                  <h3 style={{ fontSize: '1.25rem', marginBottom: '0.9rem', fontWeight: 700 }}>
                    Key Journey Highlights
                  </h3>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '0.75rem' }}>
                    {tour.highlights.map((item, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          alignItems: 'flex-start',
                          gap: '0.65rem',
                          padding: '0.75rem 1rem',
                          background: 'var(--bg-card-subtle)',
                          borderRadius: 'var(--radius-md)'
                        }}
                      >
                        <Check size={18} style={{ color: 'var(--primary)', flexShrink: 0, marginTop: '2px' }} />
                        <span style={{ fontSize: '0.88rem', color: 'var(--text-main)', lineHeight: 1.4 }}>
                          {item}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Day-by-Day Interactive Itinerary */}
              {tour.itinerary && tour.itinerary.length > 0 && (
                <div style={{ marginBottom: '2rem' }}>
                  <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem', fontWeight: 700 }}>
                    Day-by-Day Itinerary
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {tour.itinerary.map((dayItem) => {
                      const isExpanded = expandedDay === dayItem.day;
                      return (
                        <div
                          key={dayItem.day}
                          id={`itinerary-day-${dayItem.day}`}
                          style={{
                            border: '1px solid var(--border-light)',
                            borderRadius: 'var(--radius-md)',
                            overflow: 'hidden'
                          }}
                        >
                          <div
                            onClick={() => setExpandedDay(isExpanded ? null : dayItem.day)}
                            style={{
                              padding: '0.9rem 1.25rem',
                              background: isExpanded ? 'var(--bg-card-subtle)' : 'var(--bg-card)',
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'space-between',
                              userSelect: 'none'
                            }}
                          >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
                              <span style={{
                                width: '32px',
                                height: '32px',
                                borderRadius: '50%',
                                background: isExpanded ? 'var(--primary)' : 'var(--border-medium)',
                                color: '#ffffff',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '0.8rem',
                                fontWeight: 700
                              }}>
                                D{dayItem.day}
                              </span>
                              <strong style={{ fontSize: '0.95rem', color: 'var(--text-main)' }}>
                                {dayItem.title}
                              </strong>
                            </div>
                            {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                          </div>

                          {isExpanded && (
                            <div style={{
                              padding: '1rem 1.25rem 1.25rem 3.8rem',
                              color: 'var(--text-secondary)',
                              fontSize: '0.9rem',
                              lineHeight: 1.6,
                              background: 'var(--bg-card)'
                            }}>
                              {dayItem.description}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Inclusions & Exclusions */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
              }}>
                {/* Included */}
                <div style={{
                  padding: '1.25rem',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(20, 184, 166, 0.08)',
                  border: '1px solid rgba(20, 184, 166, 0.25)'
                }}>
                  <h4 style={{ color: 'var(--primary-dark)', fontWeight: 700, marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <Check size={18} /> What's Included
                  </h4>
                  <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem' }}>
                    {tour.included?.map((inc, i) => (
                      <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.4rem' }}>
                        <span style={{ color: 'var(--primary)', fontWeight: 800 }}>•</span>
                        <span>{inc}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Excluded */}
                <div style={{
                  padding: '1.25rem',
                  borderRadius: 'var(--radius-md)',
                  background: 'rgba(239, 68, 68, 0.05)',
                  border: '1px solid rgba(239, 68, 68, 0.2)'
                }}>
                  <h4 style={{ color: '#dc2626', fontWeight: 700, marginBottom: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <X size={18} /> Excluded
                  </h4>
                  <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem' }}>
                    {tour.excluded?.map((exc, i) => (
                      <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.4rem' }}>
                        <span style={{ color: '#dc2626', fontWeight: 800 }}>•</span>
                        <span>{exc}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Guest Reviews Section */}
              <div id="reviews-section" style={{ marginBottom: '2.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                    Verified Guest Experiences ({tour.reviews?.length || 0})
                  </h3>
                  <button
                    id="btn-toggle-review-form"
                    onClick={() => setShowReviewForm(!showReviewForm)}
                    className="btn-secondary"
                    style={{ padding: '0.4rem 0.85rem', fontSize: '0.82rem', gap: '0.35rem' }}
                  >
                    <MessageSquare size={14} />
                    <span>{showReviewForm ? 'Cancel' : 'Write a Review'}</span>
                  </button>
                </div>

                {reviewSuccess && (
                  <div style={{
                    padding: '0.85rem 1.25rem',
                    background: 'rgba(20, 184, 166, 0.15)',
                    color: 'var(--primary)',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '1rem',
                    fontSize: '0.88rem',
                    fontWeight: 600
                  }}>
                    ✓ Thank you! Your review has been submitted and added to this journey.
                  </div>
                )}

                {/* Add review form */}
                {showReviewForm && (
                  <form
                    id="form-add-review"
                    onSubmit={handleSubmitReview}
                    style={{
                      padding: '1.25rem',
                      background: 'var(--bg-card-subtle)',
                      borderRadius: 'var(--radius-md)',
                      marginBottom: '1.5rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.85rem'
                    }}
                  >
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.85rem' }}>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, marginBottom: '0.25rem' }}>Your Name</label>
                        <input
                          type="text"
                          required
                          value={reviewName}
                          onChange={(e) => setReviewName(e.target.value)}
                          placeholder="e.g. Julian Hayes"
                          style={{
                            width: '100%',
                            padding: '0.5rem 0.75rem',
                            borderRadius: 'var(--radius-sm)',
                            border: '1px solid var(--border-medium)',
                            background: 'var(--bg-card)'
                          }}
                        />
                      </div>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, marginBottom: '0.25rem' }}>Rating</label>
                        <select
                          value={reviewRating}
                          onChange={(e) => setReviewRating(Number(e.target.value))}
                          style={{
                            width: '100%',
                            padding: '0.5rem 0.75rem',
                            borderRadius: 'var(--radius-sm)',
                            border: '1px solid var(--border-medium)',
                            background: 'var(--bg-card)'
                          }}
                        >
                          <option value="5">★★★★★ 5 - Exceptional</option>
                          <option value="4">★★★★☆ 4 - Very Good</option>
                          <option value="3">★★★☆☆ 3 - Average</option>
                        </select>
                      </div>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, marginBottom: '0.25rem' }}>Travel Style</label>
                        <select
                          value={reviewTravelType}
                          onChange={(e) => setReviewTravelType(e.target.value)}
                          style={{
                            width: '100%',
                            padding: '0.5rem 0.75rem',
                            borderRadius: 'var(--radius-sm)',
                            border: '1px solid var(--border-medium)',
                            background: 'var(--bg-card)'
                          }}
                        >
                          <option value="Couple">Couple</option>
                          <option value="Solo">Solo Explorer</option>
                          <option value="Family">Family</option>
                          <option value="Friends">Friends Group</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, marginBottom: '0.25rem' }}>Review Title</label>
                      <input
                        type="text"
                        required
                        value={reviewTitle}
                        onChange={(e) => setReviewTitle(e.target.value)}
                        placeholder="e.g. An unforgettable week on the Amalfi Coast"
                        style={{
                          width: '100%',
                          padding: '0.5rem 0.75rem',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--border-medium)',
                          background: 'var(--bg-card)'
                        }}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, marginBottom: '0.25rem' }}>Your Experience</label>
                      <textarea
                        required
                        rows="3"
                        value={reviewComment}
                        onChange={(e) => setReviewComment(e.target.value)}
                        placeholder="What made this trip stand out? The guides, hotels, views?"
                        style={{
                          width: '100%',
                          padding: '0.5rem 0.75rem',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--border-medium)',
                          background: 'var(--bg-card)'
                        }}
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={reviewSubmitting}
                      className="btn-primary"
                      style={{ alignSelf: 'flex-start', padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
                    >
                      <Send size={14} />
                      <span>{reviewSubmitting ? 'Posting...' : 'Submit Review'}</span>
                    </button>
                  </form>
                )}

                {/* Reviews List */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {tour.reviews && tour.reviews.length > 0 ? (
                    tour.reviews.map(rev => (
                      <div
                        key={rev.id}
                        style={{
                          padding: '1.25rem',
                          borderRadius: 'var(--radius-md)',
                          background: 'var(--bg-card)',
                          border: '1px solid var(--border-light)'
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <img
                              src={rev.author_avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80'}
                              alt={rev.author_name}
                              style={{ width: '38px', height: '38px', borderRadius: '50%', objectFit: 'cover' }}
                            />
                            <div>
                              <strong style={{ fontSize: '0.9rem', color: 'var(--text-main)' }}>{rev.author_name}</strong>
                              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                {rev.travel_type} Traveller • {rev.author_country || 'Verified Guest'}
                              </div>
                            </div>
                          </div>

                          <div style={{ display: 'flex', gap: '2px', color: 'var(--accent)' }}>
                            {[...Array(rev.rating || 5)].map((_, idx) => (
                              <Star key={idx} size={14} fill="var(--accent)" />
                            ))}
                          </div>
                        </div>

                        <div style={{ fontWeight: 700, fontSize: '0.9rem', marginBottom: '0.35rem', color: 'var(--text-main)' }}>
                          "{rev.title}"
                        </div>
                        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                          {rev.comment}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No reviews yet. Be the first to review!</p>
                  )}
                </div>
              </div>
            </div>

            {/* Sticky Bottom Booking Bar */}
            <div style={{
              position: 'sticky',
              bottom: 0,
              background: 'var(--bg-glass-strong)',
              backdropFilter: 'blur(12px)',
              padding: '1rem 1.75rem',
              borderTop: '1px solid var(--border-light)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              gap: '1rem',
              zIndex: 10
            }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                  Guaranteed Departure
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.35rem' }}>
                  <span style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--text-main)', fontFamily: 'var(--font-heading)' }}>
                    {formatPrice(tour.price_per_person)}
                  </span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>/person</span>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button
                  id="btn-modal-reserve-now"
                  onClick={() => {
                    onClose();
                    onBookTour(tour);
                  }}
                  className="btn-primary"
                  style={{ padding: '0.75rem 1.85rem', fontSize: '0.95rem' }}
                >
                  Book This Expedition
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
