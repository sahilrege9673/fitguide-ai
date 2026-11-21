# Section 7: Design System, UI Tokens & Visual Language

## 1. Brand Identity: Urban Performance / Premium Athletic

FeedGuide AI embodies the physical discipline, architectural precision, and functional beauty of a high-end athletic performance laboratory. It rejects generic corporate SaaS tropes (indigo gradients, rounded purple bubbles, cartoon illustrations, glowing neon borders) in favor of high-contrast, editorial typography, purposeful negative space, razor-sharp geometric alignment, and authentic athletic data representation.

---

## 2. Strict Design Tokens & Palette

The design system permits **only** the following 6 core palette tokens. No arbitrary hex codes or alternate color classes may be introduced.

| Token Name | Hex Code | Role & Usage Restrictions | Contrast on `#171B18` |
| :--- | :--- | :--- | :--- |
| **Carbon Black** | `#171B18` | Primary dark surface, application background, primary high-contrast text. | Base Canvas |
| **Forest Green** | `#26372D` | Secondary surface, cards, table headers, containers, subtle borders. | 2.1:1 (Structural) |
| **Athletic Lime** | `#C4E76B` | Primary interactive accent, main CTAs, active indicators, key metric callouts. | **12.4:1** (AAA Pass) |
| **Warm Chalk** | `#E8E5D9` | High-contrast body text, primary display titles, clean foreground readable text. | **13.1:1** (AAA Pass) |
| **Muted Sand** | `#B5A78D` | Secondary text, uppercase tracking kickers, metadata, subtle dividers. | **5.6:1** (AA Pass) |
| **Burnt Orange** | `#C8794D` | Restrained highlights only: active workout streaks, safety warnings, alerts. | 4.6:1 (AA Pass) |

### 2.1 CSS Variables Implementation (`globals.css`)

```css
:root {
  --color-carbon-black: #171B18;
  --color-forest-green: #26372D;
  --color-athletic-lime: #C4E76B;
  --color-warm-chalk: #E8E5D9;
  --color-muted-sand: #B5A78D;
  --color-burnt-orange: #C8794D;

  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'Inter', sans-serif;

  --radius-none: 0px;
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 6px; /* Absolute maximum radius permitted */
}
```

### 2.2 Tailwind Configuration (`tailwind.config.ts`)

```typescript
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
```

---

## 3. Typography Hierarchy & Editorial Scale

- **Headings & Key Numerals**: **Space Grotesk** (Font weights: 600, 700). Characterized by geometric clarity, sharp angles, tight letter tracking (`tracking-tight` or `tracking-tighter`), and oversized scale contrasts.
- **UI & Body Copy**: **Inter** (Font weights: 400, 500, 600). Clean neutral legibility for long instructions, logs, and clinical rules.
- **Data & Metrics**: Tabular figures enabled (`font-mono` or `font-display tabular-nums`).

```
┌─────────────────┬───────────────────┬──────────────┬──────────────────────────────┐
│ Level           │ Font & Weight     │ Size / Line  │ Letter Spacing & Styling     │
├─────────────────┼───────────────────┼──────────────┼──────────────────────────────┤
│ Hero Display    │ Space Grotesk 700 │ 48px / 1.05  │ tracking-tighter uppercase   │
│ Section Title   │ Space Grotesk 600 │ 28px / 1.15  │ tracking-tight               │
│ Card Header     │ Space Grotesk 600 │ 18px / 1.25  │ tracking-tight               │
│ Eyebrow/Kicker  │ Inter 600         │ 11px / 1.0   │ tracking-widest uppercase    │
│ Primary Body    │ Inter 400         │ 14px / 1.5   │ text-chalk/90                │
│ Data Stat Num   │ Space Grotesk 700 │ 32px / 1.0   │ tabular-nums text-lime       │
│ Micro Label     │ Inter 500         │ 12px / 1.3   │ text-sand                    │
└─────────────────┴───────────────────┴──────────────┴──────────────────────────────┘
```

---

## 4. Geometry, Layout & Elevation Rules

1. **Sharp Geometry**:
   - Surfaces are crisp rectangles or minimally rounded with `rounded-sm` (2px) or `rounded-md` (max 6px).
   - **Strictly Prohibited**: `rounded-2xl`, `rounded-3xl`, pill-shaped cards (except tiny status indicator pills).
2. **Dividers Over Drop Shadows**:
   - Drop shadows and glowing colored cards are strictly prohibited.
   - Elevation is created through surface contrast (e.g., `#26372D` card on `#171B18` canvas) separated by clean 1px hairline dividers (`border border-forest` or `border border-sand/20`).
3. **Motion Guidelines**:
   - Micro-interactions (hover, focus, tab change): **150ms–200ms ease-out**.
   - Page transitions & drawer reveals: **250ms cubic-bezier(0.16, 1, 0.3, 1)**.
   - Respects `prefers-reduced-motion`: all animations instantly disabled for users requesting reduced motion.

---

## 5. Athletic Data Visualization & Restrained Charts

Charts represent physical volume, frequency, and consistency with clinical discipline:
- **No Multi-Color Rainbows**: All charts utilize only `#C4E76B` (primary metric), `#26372D` (background baseline), and `#B5A78D` (comparison/secondary).
- **Direct Labeling**: Values are rendered directly above bars or points; busy legends are omitted.
- **Zero Grid Clutter**: Horizontal grid lines are limited to 2 subtle hairline references (`stroke-[#26372D]`). Vertical grid lines are omitted.
- **Component Stack**: Lightweight custom SVG charts or SVG-based components with zero heavy external charting bloat.

---

## 6. Authentic Media & Imagery Strategy

- **Photographic Standard**: Real human athletes training with proper form in functional spaces (chalk, barbell collars, turf, natural light).
- **Prohibited Sources**:
  - Generic stock 3D AI illustrations.
  - Cartoons or stylized clip art.
  - Emoji as primary UI icons (SVG Lucide icons only).
- **Licensing & Attribution Tracking**:
  - All demonstration media must come from licensed or open-license repositories (Unsplash License, Pexels License, or Wikimedia Commons).
  - Every asset URL is linked to an exact photographer credit stored in `exercise_media` and displayed in the UI (e.g., *"Photo by Victor Freitas on Unsplash"*).
  - A permanent repository-level credit ledger is maintained in `docs/credits.md`.
