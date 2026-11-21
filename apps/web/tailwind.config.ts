import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/features/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        carbon: {
          DEFAULT: '#171B18',
          surface: '#1E2420',
          border: '#2A332C',
        },
        forest: {
          DEFAULT: '#26372D',
          light: '#2F4337',
          dark: '#1C2821',
        },
        lime: {
          DEFAULT: '#C4E76B',
          hover: '#B5DC56',
          muted: '#8AA642',
        },
        chalk: {
          DEFAULT: '#E8E5D9',
          muted: '#D0CDC0',
        },
        sand: {
          DEFAULT: '#B5A78D',
          muted: '#8A7F6A',
          divider: '#3B3830',
        },
        burnt: {
          DEFAULT: '#C8794D',
          subtle: '#4A2B1B',
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'Space Grotesk', 'sans-serif'],
        body: ['var(--font-body)', 'Inter', 'sans-serif'],
      },
      borderRadius: {
        none: '0px',
        sm: '2px',
        DEFAULT: '4px',
        md: '6px',
        lg: '6px', // Max 6px per design system guidelines
      },
      letterSpacing: {
        tightest: '-0.04em',
        tighter: '-0.02em',
        widest: '0.12em',
      },
      transitionDuration: {
        fast: '150ms',
        normal: '200ms',
        subtle: '250ms',
      },
    },
  },
  plugins: [],
};

export default config;
