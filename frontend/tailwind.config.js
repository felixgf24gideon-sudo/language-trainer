/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#1a1a1a',
          secondary: '#242424',
          tertiary: '#2a2a2a',
        },
        text: {
          primary: '#e8e8e8',
          secondary: '#9ca3af',
          muted: '#6b7280',
        },
        accent: {
          primary: '#3b82f6',
          success: '#10b981',
          error: '#ef4444',
          warning: '#f59e0b',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
