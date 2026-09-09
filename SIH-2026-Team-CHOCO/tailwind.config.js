/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Palantir Background & Surface Tiers
        background: '#1e2124',
        surface: '#000000',
        'surface-card': '#121417',
        'surface-elevated': '#16181c',
        'surface-hover': '#2f3234',
        'surface-active': '#383b3e',

        // Legacy void mappings for backward compatibility
        void: '#1e2124',
        'void-elevated': '#000000',
        'void-hover': '#2f3234',

        // Palantir Precision Borders
        border: '#636363',
        'border-subtle': 'rgba(255, 255, 255, 0.12)',
        'border-medium': '#636363',
        'border-accent': '#2b5945',

        // Palantir Typography Hierarchy
        'text-primary': '#ffffff',
        'text-secondary': '#c0c9c2',
        'text-muted': '#9b9b9b',
        'text-faint': '#636363',

        // Palantir Accents
        accent: {
          DEFAULT: '#2b5945',
          hover: '#356e56',
          light: '#3e8266',
          subtle: 'rgba(43, 89, 69, 0.15)',
        },
        'accent-gold': {
          DEFAULT: '#8c7847',
          hover: '#a68f56',
          subtle: 'rgba(140, 120, 71, 0.15)',
        },
        'telemetry-amber': '#8c7847',
        'telemetry-amber-dim': '#706037',

        // Semantic Status Colors
        danger: '#994500',
        'telemetry-red': '#ff4136',
        'telemetry-green': '#2b5945',
        'telemetry-green-bright': '#10B981',
        'telemetry-blue': '#4e8af7',
        info: '#4e8af7',
      },
      fontFamily: {
        sans: ['"Alliance No.2"', '"Hanken Grotesk"', 'system-ui', 'sans-serif'],
        display: ['"Alliance No.1"', '"Hanken Grotesk"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      fontSize: {
        '2xl': ['1.5rem', { lineHeight: '1.4' }],
        '3xl': ['1.875rem', { lineHeight: '1.4' }],
        '4xl': ['2.25rem', { lineHeight: '1.45' }],
        'display-2xl': ['clamp(2.5rem, 5vw, 4.25rem)', { lineHeight: '1.4', letterSpacing: '-0.03em', fontWeight: '700' }],
        'display-xl': ['clamp(2rem, 4vw, 3.25rem)', { lineHeight: '1.4', letterSpacing: '-0.025em', fontWeight: '700' }],
        'display-lg': ['clamp(1.5rem, 3vw, 2.25rem)', { lineHeight: '1.4', letterSpacing: '-0.02em', fontWeight: '600' }],
        'display-md': ['clamp(1.25rem, 2vw, 1.625rem)', { lineHeight: '1.4', letterSpacing: '-0.015em', fontWeight: '600' }],
        'heading-sm': ['1.125rem', { lineHeight: '1.4', letterSpacing: '-0.01em', fontWeight: '600' }],
        'body-lg': ['1.0625rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-md': ['0.9375rem', { lineHeight: '1.55', fontWeight: '400' }],
        'body-sm': ['0.8125rem', { lineHeight: '1.5', fontWeight: '400' }],
        'mono-xl': ['clamp(1.5rem, 2.5vw, 2rem)', { lineHeight: '1.4', fontWeight: '500' }],
        'mono-lg': ['1.25rem', { lineHeight: '1.4', fontWeight: '500' }],
        'mono-md': ['0.9375rem', { lineHeight: '1.4', fontWeight: '400' }],
        'mono-sm': ['0.8125rem', { lineHeight: '1.4', fontWeight: '400' }],
        'mono-xs': ['0.75rem', { lineHeight: '1.4', letterSpacing: '0.04em', fontWeight: '500' }],
      },
      borderRadius: {
        'card': '17px',
        'btn': '2px',       // Sharp Palantir button corners
        'input': '2px',     // Sharp industrial form controls
        'badge': '2px',     // Crisp technical badge rectangles
        'pill': '9999px',
        'sharp': '0px',
      },
      boxShadow: {
        'focus': '0 0 0 1px #2b5945',
        'focus-gold': '0 0 0 1px #8c7847',
        'floating': '0px 2px 10px 0px rgba(0, 0, 0, 0.5)',
      },
      transitionDuration: {
        DEFAULT: '150ms',
      },
      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
        '20': '80px',
      },
    },
  },
  plugins: [],
}