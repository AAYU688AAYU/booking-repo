const RAW_API_BASE = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/+$/, '');
const API_BASE = RAW_API_BASE.endsWith('/api') ? RAW_API_BASE : (RAW_API_BASE === '' ? '/api' : `${RAW_API_BASE}/api`);

export const api = {
  // Get all destinations
  async getDestinations() {
    const res = await fetch(`${API_BASE}/destinations/`);
    if (!res.ok) throw new Error('Failed to fetch destinations');
    return res.json();
  },

  // Get trips with optional query parameters
  async getTrips(params = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '' && value !== 'All') {
        query.append(key, value);
      }
    });

    const queryString = query.toString();
    const url = `${API_BASE}/trips/${queryString ? `?${queryString}` : ''}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch trips');
    return res.json();
  },

  // Get single trip detail by ID
  async getTripDetail(id) {
    const res = await fetch(`${API_BASE}/trips/${id}/`);
    if (!res.ok) throw new Error('Failed to fetch trip details');
    return res.json();
  },

  // Create booking
  async createBooking(bookingData) {
    const res = await fetch(`${API_BASE}/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.guests_count || 'Booking failed');
    }
    return res.json();
  },

  // Search bookings by email or reference
  async getBookings({ email, reference }) {
    const query = new URLSearchParams();
    if (email) query.append('email', email);
    if (reference) query.append('reference', reference);

    const res = await fetch(`${API_BASE}/bookings/?${query.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch bookings');
    return res.json();
  },

  // Add review for a tour
  async addReview(tourId, reviewData) {
    const res = await fetch(`${API_BASE}/trips/${tourId}/reviews/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(reviewData),
    });
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to submit review');
    }
    return res.json();
  },

  // Get platform stats
  async getStats() {
    const res = await fetch(`${API_BASE}/stats/`);
    if (!res.ok) throw new Error('Failed to fetch platform stats');
    return res.json();
  },
};
