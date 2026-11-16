import React, { createContext, useContext, useState, useEffect } from 'react';

const TravelContext = createContext();

const CURRENCY_RATES = {
  INR: { symbol: '₹', rate: 84.5, label: 'INR (₹)' },
  USD: { symbol: '$', rate: 1.0, label: 'USD ($)' },
  EUR: { symbol: '€', rate: 0.92, label: 'EUR (€)' },
  GBP: { symbol: '£', rate: 0.79, label: 'GBP (£)' },
  AUD: { symbol: 'A$', rate: 1.52, label: 'AUD (A$)' },
};

export function TravelProvider({ children }) {
  // Theme state: dark / light
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('voyage_theme') || 'light';
  });

  // Currency state (defaults to INR for authentic local pricing)
  const [currency, setCurrency] = useState(() => {
    return localStorage.getItem('voyage_currency') || 'INR';
  });

  // Wishlist state: array of tour IDs
  const [wishlist, setWishlist] = useState(() => {
    try {
      const saved = localStorage.getItem('voyage_wishlist');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Active user bookings stored locally for instant recovery
  const [myBookingRefs, setMyBookingRefs] = useState(() => {
    try {
      const saved = localStorage.getItem('voyage_my_bookings');
      return saved ? JSON.parse(saved) : ['TRV-30092', 'TRV-42407'];
    } catch {
      return ['TRV-30092', 'TRV-42407'];
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('voyage_theme', theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem('voyage_currency', currency);
  }, [currency]);

  useEffect(() => {
    localStorage.setItem('voyage_wishlist', JSON.stringify(wishlist));
  }, [wishlist]);

  useEffect(() => {
    localStorage.setItem('voyage_my_bookings', JSON.stringify(myBookingRefs));
  }, [myBookingRefs]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  const toggleWishlist = (tourId) => {
    setWishlist(prev => {
      if (prev.includes(tourId)) {
        return prev.filter(id => id !== tourId);
      }
      return [...prev, tourId];
    });
  };

  const isWishlisted = (tourId) => wishlist.includes(tourId);

  const addBookingRef = (ref) => {
    if (!myBookingRefs.includes(ref)) {
      setMyBookingRefs(prev => [ref, ...prev]);
    }
  };

  const formatPrice = (amountInUSD) => {
    const num = typeof amountInUSD === 'number' ? amountInUSD : parseFloat(amountInUSD) || 0;
    const config = CURRENCY_RATES[currency] || CURRENCY_RATES.USD;
    const converted = Math.round(num * config.rate);
    return `${config.symbol}${converted.toLocaleString()}`;
  };

  return (
    <TravelContext.Provider
      value={{
        theme,
        toggleTheme,
        currency,
        setCurrency,
        currencies: CURRENCY_RATES,
        wishlist,
        toggleWishlist,
        isWishlisted,
        myBookingRefs,
        addBookingRef,
        formatPrice,
      }}
    >
      {children}
    </TravelContext.Provider>
  );
}

export function useTravel() {
  const context = useContext(TravelContext);
  if (!context) {
    throw new Error('useTravel must be used within TravelProvider');
  }
  return context;
}
