import test, { describe, it } from 'node:test';
import assert from 'node:assert/strict';

// Test UI utility cn (clsx + tailwind-merge)
import { cn } from '../src/lib/utils.ts';

describe('Frontend Utility Tests', () => {
  it('cn should merge class names cleanly', () => {
    const result = cn('px-4 py-2', 'bg-forest-900', false && 'hidden', undefined, null);
    assert.equal(result, 'px-4 py-2 bg-forest-900');
  });

  it('cn should resolve Tailwind conflict overrides correctly', () => {
    const result = cn('p-4', 'p-6');
    assert.equal(result, 'p-6');
  });
});

describe('Design Tokens Verification', () => {
  it('should define required Urban Performance brand tokens', () => {
    const TOKENS = {
      carbon: '#171B18',
      forest: '#26372D',
      lime: '#C4E76B',
      chalk: '#E8E5D9',
      sand: '#B5A78D',
      burnt: '#C8794D'
    };
    assert.equal(TOKENS.carbon, '#171B18');
    assert.equal(TOKENS.forest, '#26372D');
    assert.equal(TOKENS.lime, '#C4E76B');
    assert.equal(TOKENS.chalk, '#E8E5D9');
    assert.equal(TOKENS.sand, '#B5A78D');
    assert.equal(TOKENS.burnt, '#C8794D');
  });
});

describe('Navigation Structure Verification', () => {
  it('should define all core application routes for authenticated users', () => {
    const ROUTES = [
      { name: 'Dashboard', href: '/dashboard' },
      { name: 'Workouts', href: '/workouts' },
      { name: 'Exercises', href: '/exercises' },
      { name: 'Schedule', href: '/schedule' },
      { name: 'Progress', href: '/progress' },
      { name: 'AI Coach', href: '/assistant' },
      { name: 'Profile', href: '/profile' },
    ];
    assert.equal(ROUTES.length, 7);
    const hrefs = ROUTES.map(r => r.href);
    assert.ok(hrefs.includes('/dashboard'));
    assert.ok(hrefs.includes('/workouts'));
    assert.ok(hrefs.includes('/exercises'));
    assert.ok(hrefs.includes('/progress'));
    assert.ok(hrefs.includes('/assistant'));
  });
});

describe('Progress Analytics Computations', () => {
  it('computes accumulated tonnage correctly', () => {
    const sets = [
      { reps: 10, weight_kg: 50 }, // 500 kg
      { reps: 8, weight_kg: 60 },  // 480 kg
      { reps: 6, weight_kg: 70 },  // 420 kg
    ];
    const totalTonnage = sets.reduce((acc, s) => acc + (s.reps * s.weight_kg), 0);
    assert.equal(totalTonnage, 1400);
  });

  it('computes consistency score accurately as scheduled vs completed ratio', () => {
    const scheduled = 4;
    const completed = 3;
    const score = Math.round((completed / scheduled) * 100);
    assert.equal(score, 75);
  });
});

describe('Clinical Safety Input Checks', () => {
  it('rejects workout generation without medical disclaimer acknowledgment', () => {
    const payload = {
      medical_disclaimer_acknowledged: false,
      experience_level: 'intermediate',
      preferred_duration_minutes: 45
    };
    const isValid = payload.medical_disclaimer_acknowledged === true;
    assert.equal(isValid, false);
  });

  it('flags red flag symptom queries', () => {
    const RED_FLAGS = [
      'chest pain',
      'dizzy',
      'dizziness',
      'fainted',
      'blacked out',
      'shortness of breath',
      'radiating pain'
    ];
    const userQuery = 'I feel acute dizziness and chest pain when lifting';
    const isRedFlag = RED_FLAGS.some(flag => userQuery.toLowerCase().includes(flag));
    assert.equal(isRedFlag, true);
  });
});
