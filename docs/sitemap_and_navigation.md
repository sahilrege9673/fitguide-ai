# Section 2: Sitemap, Page Hierarchy & UX States

## 1. Information Architecture & Route Tree

FitGuide AI utilizes Next.js App Router with segregated route groups to guarantee clean layout inheritance, strict middleware session verification, and clear separation of public, onboarding, and authenticated application states.

```
/ (Root)
│
├── / (Public Marketing & Landing)
│   ├── page.tsx                       [Public] High-conversion editorial landing page
│   └── layout.tsx                     [Public] Header with CTA + Footer with disclaimer & credits
│
├── (auth)/                            [Guest-Only Route Group]
│   ├── /login                         [Guest] Email/Password + Google OAuth
│   ├── /register                      [Guest] Registration with immediate email verification trigger
│   ├── /forgot-password               [Guest] Password reset request
│   ├── /auth/callback                 [Callback] Supabase OAuth & Magic link PKCE code exchange
│   └── /auth/reset-password           [Authenticated/Token] Secure new password entry
│
├── (onboarding)/                      [Authenticated Guarded Route Group]
│   └── /onboarding                    [Guarded] 6-step wizard: Age, Goals, Experience, Gear, Days, Time
│                                      - Persistent state via Supabase draft auto-save
│                                      - Mandatory safety disclaimer acceptance
│                                      - Redirects to /dashboard upon completion
│
└── (dashboard)/                       [Authenticated Protected App Shell]
    ├── layout.tsx                     [Shell] Persistent Desktop Left Rail / Mobile Bottom Tab Bar
    │
    ├── /dashboard                     [Primary Hub] Today's workout, weekly completion ring, AI alert
    │
    ├── /workouts                      [Workout Management]
    │   ├── page.tsx                   Current active weekly plan & recent history
    │   ├── /[id]                      Day-specific workout execution player & active logger
    │   └── /[id]/summary              Post-workout feedback & metrics summary
    │
    ├── /exercises                     [Knowledge & Discovery]
    │   ├── page.tsx                   Searchable & filterable library (>= 80 verified exercises)
    │   └── /[slug]                    Detailed exercise view: biomechanics, video/media, contraindications
    │
    ├── /assistant                     [Conversational AI]
    │   ├── page.tsx                   Interactive streaming chat grounded in live user profile
    │   └── /[conversationId]          Historical conversation thread review
    │
    ├── /schedule                      [Weekly Planning]
    │   └── page.tsx                   Interactive 7-day calendar, rest day balancer, workout rescheduler
    │
    ├── /progress                      [Analytics & Reports]
    │   ├── page.tsx                   Restrained athletic charts: consistency index, muscle volume, trends
    │   └── /report/download           PDF generation and download route
    │
    └── /profile                       [Account & Settings]
        ├── page.tsx                   Personal details & fitness preference modifier
        ├── /security                  Password update & active sessions
        └── /data-privacy              GDPR/CCPA JSON data export & cascade account deletion
```

---

## 2. Navigation Architecture: Desktop Rail vs. Mobile Bottom Nav

To deliver an authentic athletic tech experience that feels native on both mobile devices and wide desktop displays, FitGuide AI employs distinct navigation paradigms:

### 2.1 Desktop Navigation (Viewport >= 1024px)
- **Persistent Left Rail**: Fixed width (256px), dark surface (`#171B18`), subtle border (`#26372D`).
- **Brand Header**: Minimalist FitGuide AI wordmark with Athletic Lime (`#C4E76B`) status indicator.
- **Primary Nav Links**:
  1. **Dashboard** (`/dashboard`)
  2. **Workouts** (`/workouts`)
  3. **Schedule** (`/schedule`)
  4. **Exercises** (`/exercises`)
  5. **AI Assistant** (`/assistant`)
  6. **Progress** (`/progress`)
- **Utility Footer**: User avatar, active goal badge, and Settings (`/profile`) link.
- **Quick Action Bar**: "Start Today's Workout" persistent Athletic Lime accent button.

### 2.2 Mobile Navigation (Viewport < 1024px)
- **Top Brand Bar**: Compact 56px sticky bar featuring brand mark, safety status badge, and profile thumbnail.
- **Fixed Bottom Tab Bar**: 64px thumb-friendly bar fixed to viewport bottom with safe-area padding (`pb-safe`).
  - **5 Primary Touch Targets** (minimum 48x48px hit area):
    1. **Home** (`/dashboard`)
    2. **Workouts** (`/workouts`)
    3. **Schedule** (`/schedule`)
    4. **AI Coach** (`/assistant`)
    5. **More** (Drawer sheet housing *Exercises*, *Progress*, *Profile*, and *Safety Rules*)

---

## 3. Four-State UI Architecture (Universal Contract)

Every functional screen across the application strictly implements all four UI lifecycle states to eliminate layout shifts and ambiguous user states:

```
┌────────────────────────────────────────────────────────┐
│                   State Machine Contract               │
├─────────────────┬──────────────────────────────────────┤
│ 1. Loading      │ Bespoke skeleton matching real wire  │
│ 2. Empty        │ Contextual explanation + single CTA  │
│ 3. Error        │ Clean diagnostic + retry button      │
│ 4. Success      │ High-density athletic data render    │
└─────────────────┴──────────────────────────────────────┘
```

### 3.1 Loading State (Bespoke Skeletons)
- Skeletons use `#26372D` base with a subtle shimmer animation (1.8s linear loop).
- Skeletons replicate the exact spatial dimensions of typography, stat tiles, and cards to eliminate Cumulative Layout Shift (CLS < 0.05).
- Never use generic spinning circular loaders for content areas.

### 3.2 Empty State
- Rendered when a dataset contains zero records (e.g., no completed workouts yet, empty chat history, no workouts scheduled on rest day).
- Layout:
  1. Small uppercase category kicker (`text-[#B5A78D]` tracking-widest).
  2. Direct, confident headline (`font-display font-bold text-[#E8E5D9]`).
  3. One single, prominent call-to-action button in Athletic Lime (`#C4E76B`).
  4. Zero playful generic illustrations or emojis.

### 3.3 Error State
- Triggered on API failure, network partition, or validation rejection.
- Layout:
  1. Restrained alert container with subtle Burnt Orange border (`#C8794D`).
  2. Clear, human-readable error description (zero raw stack traces or internal codes).
  3. Deterministic action button: "Retry Request" or "Re-authenticate".

### 3.4 Success / Data State
- Editorial grid typography, tabular numerals for reps/sets/dates, high-contrast dark theme surfaces.

---

## 4. Accessibility & Responsive Specifications

- **Contrast Ratios**: All text combinations meet or exceed WCAG AA (minimum 4.5:1 for body copy, 3:1 for large display headers).
  - Athletic Lime (`#C4E76B`) on Carbon Black (`#171B18`): **12.4:1** (WCAG AAA Pass).
  - Warm Chalk (`#E8E5D9`) on Forest Green (`#26372D`): **9.8:1** (WCAG AAA Pass).
  - Muted Sand (`#B5A78D`) on Carbon Black (`#171B18`): **5.6:1** (WCAG AA Pass).
- **Focus Rings**: Universal keyboard focus ring: `outline: 2px solid #C4E76B; outline-offset: 2px;`.
- **Keyboard Navigation**: Full tab index traversal for all modals, drawers, calendar days, and workout logger inputs.
- **Semantic HTML**: Strict usage of `<main>`, `<nav>`, `<aside>`, `<section>`, `<article>`, and `<header>` tags. Zero `div`-soup buttons.
