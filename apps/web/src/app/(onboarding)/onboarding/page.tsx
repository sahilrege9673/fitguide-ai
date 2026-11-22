'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient, ApiError } from '@/lib/api/client';
import { createClient } from '@/lib/supabase/client';
import { 
  ShieldCheck, 
  Target, 
  Clock, 
  Calendar, 
  Dumbbell, 
  AlertTriangle, 
  Check, 
  ArrowRight, 
  ArrowLeft 
} from 'lucide-react';

type AgeGroup = 'minor_under_18' | 'adult_18_64' | 'senior_65_plus';
type ExperienceLevel = 'beginner' | 'intermediate' | 'advanced';

interface OnboardingFormState {
  age_group: AgeGroup;
  experience_level: ExperienceLevel;
  fitness_goals: string[];
  workout_location: string;
  available_equipment: string[];
  preferred_activities: string[];
  time_availability_mins: number;
  preferred_days: number[];
  disclaimer_accepted: boolean;
}

const DEFAULT_STATE: OnboardingFormState = {
  age_group: 'adult_18_64',
  experience_level: 'intermediate',
  fitness_goals: ['strength', 'hypertrophy'],
  workout_location: 'commercial_gym',
  available_equipment: ['barbell', 'dumbbells', 'cable_machine', 'bench'],
  preferred_activities: ['weightlifting'],
  time_availability_mins: 45,
  preferred_days: [1, 3, 5],
  disclaimer_accepted: false,
};

const STEPS = [
  { id: 1, name: 'Age & Physiology' },
  { id: 2, name: 'Goals & Experience' },
  { id: 3, name: 'Location & Equipment' },
  { id: 4, name: 'Time & Schedule' },
  { id: 5, name: 'Safety Screening' },
  { id: 6, name: 'Confirmation' },
];

const DAYS = [
  { id: 1, label: 'Mon' },
  { id: 2, label: 'Tue' },
  { id: 3, label: 'Wed' },
  { id: 4, label: 'Thu' },
  { id: 5, label: 'Fri' },
  { id: 6, label: 'Sat' },
  { id: 7, label: 'Sun' },
];

export default function OnboardingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = React.useState(1);
  const [formData, setFormData] = React.useState<OnboardingFormState>(DEFAULT_STATE);
  const [isInitializing, setIsInitializing] = React.useState(true);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  // Load existing draft or preferences
  React.useEffect(() => {
    async function loadInitialData() {
      try {
        const supabase = createClient();
        const { data: { session } } = await supabase.auth.getSession();
        if (!session) {
          router.push('/login');
          return;
        }

        // Try to load saved draft from local storage
        const savedDraft = localStorage.getItem('fitguide_onboarding_draft');
        if (savedDraft) {
          try {
            setFormData(JSON.parse(savedDraft));
          } catch {
            // ignore JSON error
          }
        }

        // Check if backend already has saved preferences
        const remotePrefs = await apiClient<any>('/onboarding').catch(() => null);
        if (remotePrefs && remotePrefs.completed_at) {
          router.push('/dashboard');
          return;
        } else if (remotePrefs) {
          setFormData((prev) => ({ ...prev, ...remotePrefs }));
        }
      } catch (err) {
        console.warn('Initial onboarding check failed:', err);
      } finally {
        setIsInitializing(false);
      }
    }

    loadInitialData();
  }, [router]);

  // Auto-save draft locally on change
  const updateForm = (updates: Partial<OnboardingFormState>) => {
    setFormData((prev) => {
      const next = { ...prev, ...updates };
      localStorage.setItem('fitguide_onboarding_draft', JSON.stringify(next));
      return next;
    });
  };

  const toggleArrayItem = (key: 'fitness_goals' | 'available_equipment' | 'preferred_activities', item: string) => {
    const list = formData[key];
    const nextList = list.includes(item) ? list.filter((i) => i !== item) : [...list, item];
    updateForm({ [key]: nextList });
  };

  const toggleDay = (dayId: number) => {
    const days = formData.preferred_days;
    const nextDays = days.includes(dayId) ? days.filter((d) => d !== dayId) : [...days, dayId];
    if (nextDays.length === 0) return; // Keep at least 1 day
    updateForm({ preferred_days: nextDays.sort() });
  };

  const handleNext = () => {
    setErrorMsg(null);

    // Step-specific validations
    if (currentStep === 2 && formData.fitness_goals.length === 0) {
      setErrorMsg('Please select at least one primary fitness goal.');
      return;
    }
    if (currentStep === 4 && formData.preferred_days.length === 0) {
      setErrorMsg('Please select at least one workout day per week.');
      return;
    }
    if (currentStep === 5 && !formData.disclaimer_accepted) {
      setErrorMsg('You must review and accept the fitness disclaimer to proceed.');
      return;
    }

    if (currentStep < 6) {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    setErrorMsg(null);
    if (currentStep > 1) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    setErrorMsg(null);

    try {
      await apiClient('/onboarding', {
        method: 'POST',
        body: JSON.stringify(formData),
      });

      localStorage.removeItem('fitguide_onboarding_draft');
      router.push('/dashboard');
      router.refresh();
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg('Failed to save onboarding configuration. Please retry.');
      }
      setIsSubmitting(false);
    }
  };

  if (isInitializing) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-carbon px-4">
        <div className="w-full max-w-xl space-y-4">
          <Skeleton className="h-6 w-32" />
          <Skeleton className="h-12 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-carbon px-4 py-12 flex flex-col items-center justify-center">
      <div className="w-full max-w-2xl space-y-8">
        
        {/* Header & Step Tracker */}
        <div className="space-y-4 text-center">
          <div className="inline-flex items-center gap-2">
            <span className="h-2.5 w-2.5 bg-lime" />
            <span className="font-display text-lg font-bold tracking-tight text-chalk">
              FITGUIDE<span className="text-lime">.AI</span> // ATHLETE ONBOARDING
            </span>
          </div>

          {/* Stepper Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs font-mono uppercase tracking-widest text-sand">
              <span>Step {currentStep} of 6: {STEPS[currentStep - 1].name}</span>
              <span className="text-lime">{Math.round((currentStep / 6) * 100)}%</span>
            </div>
            <div className="h-1.5 w-full bg-forest rounded-none overflow-hidden">
              <div 
                className="h-full bg-lime transition-all duration-normal"
                style={{ width: `${(currentStep / 6) * 100}%` }}
              />
            </div>
          </div>
        </div>

        {errorMsg && (
          <Alert variant="error" title="Validation Alert">
            {errorMsg}
          </Alert>
        )}

        {/* STEP 1: Age & Physiology */}
        {currentStep === 1 && (
          <Card>
            <CardHeader>
              <CardTitle>Biological Age &amp; Category</CardTitle>
              <CardDescription>
                FitGuide AI enforces age-specific clinical guardrails. Minors receive motor-skill programming with zero 1RM max-effort lifting. Seniors receive fall-prevention and low-impact work.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  {
                    id: 'minor_under_18' as AgeGroup,
                    title: 'Under 18',
                    desc: 'Form-focused mechanics, bodyweight foundations, strictly no max lifts or calorie cuts.',
                  },
                  {
                    id: 'adult_18_64' as AgeGroup,
                    title: '18 — 64',
                    desc: 'Progressive overload, periodized strength, hypertrophy, and conditioning.',
                  },
                  {
                    id: 'senior_65_plus' as AgeGroup,
                    title: '65+',
                    desc: 'Joint-friendly mobility, balance, fall prevention, and low-impact volume.',
                  },
                ].map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => updateForm({ age_group: item.id })}
                    className={`p-4 text-left border rounded-sm transition-all duration-fast ${
                      formData.age_group === item.id
                        ? 'border-lime bg-forest/40 text-chalk'
                        : 'border-forest bg-carbon-surface text-sand hover:border-sand/40'
                    }`}
                  >
                    <div className="font-display font-bold uppercase text-sm mb-1 flex items-center justify-between">
                      {item.title}
                      {formData.age_group === item.id && <Check className="h-4 w-4 text-lime" />}
                    </div>
                    <p className="text-xs leading-relaxed text-sand/80">{item.desc}</p>
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* STEP 2: Goals & Experience */}
        {currentStep === 2 && (
          <Card>
            <CardHeader>
              <CardTitle>Experience Level &amp; Primary Objectives</CardTitle>
              <CardDescription>
                Select your training tenure and up to 3 core physical objectives.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-mono uppercase tracking-wider text-sand">Experience Level</label>
                <div className="grid grid-cols-3 gap-3">
                  {(['beginner', 'intermediate', 'advanced'] as ExperienceLevel[]).map((level) => (
                    <button
                      key={level}
                      type="button"
                      onClick={() => updateForm({ experience_level: level })}
                      className={`py-3 text-center border rounded-sm font-display uppercase text-xs font-semibold tracking-wider transition-colors duration-fast ${
                        formData.experience_level === level
                          ? 'border-lime bg-lime text-carbon'
                          : 'border-forest bg-carbon-surface text-sand hover:text-chalk'
                      }`}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-mono uppercase tracking-wider text-sand">Fitness Goals (Select All That Apply)</label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
                  {[
                    { id: 'strength', label: 'Maximum Strength' },
                    { id: 'hypertrophy', label: 'Muscle Hypertrophy' },
                    { id: 'endurance', label: 'Stamina & Aerobic' },
                    { id: 'mobility', label: 'Joint Mobility' },
                    { id: 'athletic_power', label: 'Athletic Power' },
                    { id: 'longevity', label: 'Metabolic Health' },
                  ].map((goal) => {
                    const isSelected = formData.fitness_goals.includes(goal.id);
                    return (
                      <button
                        key={goal.id}
                        type="button"
                        onClick={() => toggleArrayItem('fitness_goals', goal.id)}
                        className={`p-3 text-left border rounded-sm text-xs font-mono transition-colors duration-fast flex items-center justify-between ${
                          isSelected
                            ? 'border-lime bg-forest/40 text-chalk'
                            : 'border-forest bg-carbon-surface text-sand hover:border-sand/40'
                        }`}
                      >
                        <span>{goal.label}</span>
                        {isSelected && <Check className="h-3.5 w-3.5 text-lime" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* STEP 3: Location & Equipment */}
        {currentStep === 3 && (
          <Card>
            <CardHeader>
              <CardTitle>Training Environment &amp; Gear</CardTitle>
              <CardDescription>
                We only generate exercises using gear you actually possess.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-mono uppercase tracking-wider text-sand">Primary Location</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                  {[
                    { id: 'commercial_gym', label: 'Commercial Gym' },
                    { id: 'home_gym', label: 'Home Gym' },
                    { id: 'outdoor', label: 'Outdoor Turf' },
                    { id: 'bodyweight_only', label: 'Calisthenics Space' },
                  ].map((loc) => (
                    <button
                      key={loc.id}
                      type="button"
                      onClick={() => updateForm({ workout_location: loc.id })}
                      className={`p-3 text-center border rounded-sm text-xs font-mono transition-colors duration-fast ${
                        formData.workout_location === loc.id
                          ? 'border-lime bg-forest/50 text-chalk'
                          : 'border-forest bg-carbon-surface text-sand hover:text-chalk'
                      }`}
                    >
                      {loc.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-mono uppercase tracking-wider text-sand">Available Equipment</label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {[
                    { id: 'barbell', label: 'Barbell & Plates' },
                    { id: 'dumbbells', label: 'Dumbbells' },
                    { id: 'cable_machine', label: 'Cable Machine' },
                    { id: 'bench', label: 'Adjustable Bench' },
                    { id: 'pull_up_bar', label: 'Pull-Up Bar' },
                    { id: 'kettlebells', label: 'Kettlebells' },
                    { id: 'resistance_bands', label: 'Resistance Bands' },
                    { id: 'bodyweight', label: 'Bodyweight Only' },
                  ].map((gear) => {
                    const isSelected = formData.available_equipment.includes(gear.id);
                    return (
                      <button
                        key={gear.id}
                        type="button"
                        onClick={() => toggleArrayItem('available_equipment', gear.id)}
                        className={`p-2.5 text-left border rounded-sm text-xs font-mono transition-colors duration-fast flex items-center justify-between ${
                          isSelected
                            ? 'border-lime bg-forest/40 text-chalk'
                            : 'border-forest bg-carbon-surface text-sand hover:border-sand/40'
                        }`}
                      >
                        <span className="truncate">{gear.label}</span>
                        {isSelected && <Check className="h-3 w-3 text-lime shrink-0 ml-1" />}
                      </button>
                    );
                  })}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* STEP 4: Time & Schedule */}
        {currentStep === 4 && (
          <Card>
            <CardHeader>
              <CardTitle>Session Duration &amp; Training Days</CardTitle>
              <CardDescription>
                Calibrate your weekly calendar volume to match your lifestyle commitments.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <label className="text-xs font-mono uppercase tracking-wider text-sand">Available Time per Session</label>
                  <span className="font-display font-bold text-lime tabular-nums text-lg">
                    {formData.time_availability_mins} MINS
                  </span>
                </div>
                <input
                  type="range"
                  min={15}
                  max={90}
                  step={15}
                  value={formData.time_availability_mins}
                  onChange={(e) => updateForm({ time_availability_mins: parseInt(e.target.value) })}
                  className="w-full accent-[#C4E76B] bg-forest h-2 rounded-none cursor-pointer"
                />
                <div className="flex justify-between text-[10px] font-mono text-sand">
                  <span>15 Mins (Express)</span>
                  <span>45 Mins (Standard)</span>
                  <span>90 Mins (Comprehensive)</span>
                </div>
              </div>

              <div className="space-y-2 pt-4 border-t border-forest/40">
                <label className="text-xs font-mono uppercase tracking-wider text-sand">
                  Preferred Training Days (Select {formData.preferred_days.length} Active Days)
                </label>
                <div className="grid grid-cols-7 gap-1.5 sm:gap-2">
                  {DAYS.map((day) => {
                    const isSelected = formData.preferred_days.includes(day.id);
                    return (
                      <button
                        key={day.id}
                        type="button"
                        onClick={() => toggleDay(day.id)}
                        className={`py-3 text-center border rounded-sm font-display text-xs font-bold uppercase transition-colors duration-fast ${
                          isSelected
                            ? 'border-lime bg-lime text-carbon'
                            : 'border-forest bg-carbon-surface text-sand hover:text-chalk'
                        }`}
                      >
                        {day.label}
                      </button>
                    );
                  })}
                </div>
                <p className="text-[11px] font-mono text-sand/80 mt-1">
                  Unselected days are programmed as restorative active recovery or rest days.
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* STEP 5: Safety Screening & Mandatory Disclaimer */}
        {currentStep === 5 && (
          <Card className="border-burnt/30">
            <CardHeader>
              <div className="flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-burnt" />
                <CardTitle>Clinical Safety &amp; Invariant Check</CardTitle>
              </div>
              <CardDescription>
                Confirm your medical suitability before we generate physical routines.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-carbon p-4 rounded-sm border border-forest space-y-3 text-xs text-sand leading-relaxed">
                <p className="text-chalk font-semibold uppercase font-mono">
                  [ SCREENING FOR CARDIOVASCULAR &amp; ACUTE CONDITIONS ]
                </p>
                <p>
                  Do you currently experience chest pain, unexplained dizziness or syncope during exercise, acute ligament or joint pain, or unmanaged chronic cardiovascular symptoms?
                </p>
                <p className="text-burnt font-mono">
                  &gt; If YES: You must not proceed. Please seek immediate evaluation from a licensed medical physician.
                </p>
              </div>

              {/* Mandatory Fitness Disclaimer */}
              <div className="border border-forest p-4 rounded-sm bg-forest/20 space-y-3">
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    id="disclaimer-checkbox"
                    checked={formData.disclaimer_accepted}
                    onChange={(e) => updateForm({ disclaimer_accepted: e.target.checked })}
                    className="mt-1 h-4 w-4 rounded-none accent-[#C4E76B] bg-carbon border-forest cursor-pointer"
                  />
                  <label htmlFor="disclaimer-checkbox" className="text-xs text-chalk leading-relaxed cursor-pointer select-none">
                    <span className="font-semibold text-lime">I acknowledge and accept the Health &amp; Fitness Disclaimer:</span>{' '}
                    FitGuide AI provides evidence-based athletic guidance and activity tracking for general wellness. It is not a clinical medical service, physical therapy clinic, or emergency diagnostic tool. I certify that I am physically fit to participate in progressive exercise or have received medical clearance.
                  </label>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* STEP 6: Summary & Confirmation */}
        {currentStep === 6 && (
          <Card>
            <CardHeader>
              <CardTitle>Profile Review &amp; Activation</CardTitle>
              <CardDescription>
                Review your parameters before we compile your initial weekly cycle.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 font-mono text-xs">
              <div className="grid grid-cols-2 gap-3 bg-carbon p-4 rounded-sm border border-forest">
                <div>
                  <span className="text-sand uppercase">Physiology:</span>
                  <p className="text-chalk font-semibold mt-0.5">{formData.age_group.replace('_', ' ')}</p>
                </div>
                <div>
                  <span className="text-sand uppercase">Experience:</span>
                  <p className="text-chalk font-semibold mt-0.5 uppercase">{formData.experience_level}</p>
                </div>
                <div>
                  <span className="text-sand uppercase">Session Duration:</span>
                  <p className="text-lime font-semibold mt-0.5">{formData.time_availability_mins} Minutes</p>
                </div>
                <div>
                  <span className="text-sand uppercase">Active Days:</span>
                  <p className="text-chalk font-semibold mt-0.5">{formData.preferred_days.length} Days / Week</p>
                </div>
                <div className="col-span-2">
                  <span className="text-sand uppercase">Primary Goals:</span>
                  <p className="text-chalk font-semibold mt-0.5">{formData.fitness_goals.join(', ')}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 text-lime font-mono text-xs">
                <Check className="h-4 w-4" />
                <span>Safety invariants accepted. Database RLS isolation active.</span>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between border-t border-forest pt-6">
          <Button
            type="button"
            variant="outline"
            onClick={handleBack}
            disabled={currentStep === 1 || isSubmitting}
          >
            <ArrowLeft className="mr-2 h-4 w-4" /> Previous
          </Button>

          {currentStep < 6 ? (
            <Button
              type="button"
              variant="primary"
              onClick={handleNext}
            >
              Continue <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button
              type="button"
              variant="primary"
              onClick={handleSubmit}
              isLoading={isSubmitting}
            >
              Finalize Assessment &amp; Enter Lab <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          )}
        </div>

      </div>
    </div>
  );
}
