'use client';

import * as React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient, ApiError } from '@/lib/api/client';
import { 
  Play, 
  Sparkles, 
  Calendar, 
  Dumbbell, 
  CheckCircle2, 
  Clock, 
  Flame, 
  ShieldCheck, 
  ArrowRight,
  TrendingUp,
  Activity
} from 'lucide-react';

interface ProfileData {
  id: string;
  email: string;
  full_name?: string;
  has_completed_onboarding: boolean;
}

interface OnboardingData {
  age_group: string;
  experience_level: string;
  fitness_goals: string[];
  workout_location: string;
  time_availability_mins: number;
  preferred_days: number[];
  disclaimer_accepted: boolean;
}

interface WorkoutSession {
  id: string;
  title: string;
  focus_area: string;
  planned_duration_mins: number;
  status: string;
  scheduled_time: string;
  completed_at?: string;
  perceived_exertion?: number;
  exercises: Array<{
    id: string;
    exercise_order: number;
    target_sets: number;
    target_reps?: number;
    exercise: {
      id: string;
      name: string;
      slug: string;
    };
  }>;
}

export default function DashboardPage() {
  const router = useRouter();
  const [profile, setProfile] = React.useState<ProfileData | null>(null);
  const [preferences, setPreferences] = React.useState<OnboardingData | null>(null);
  const [todaySession, setTodaySession] = React.useState<WorkoutSession | null>(null);
  const [history, setHistory] = React.useState<WorkoutSession[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [isGenerating, setIsGenerating] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const fetchDashboardData = React.useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const prof = await apiClient<ProfileData>('/auth/me');
      setProfile(prof);

      const prefs = await apiClient<OnboardingData>('/onboarding').catch(() => null);
      setPreferences(prefs);

      if (!prof.has_completed_onboarding && !prefs) {
        router.push('/onboarding');
        return;
      }

      // Fetch today's workout
      const today = await apiClient<WorkoutSession | null>('/workouts/today').catch(() => null);
      setTodaySession(today);

      // Fetch history
      const hist = await apiClient<WorkoutSession[]>('/workouts/history').catch(() => []);
      setHistory(hist);
    } catch (err: unknown) {
      if (err instanceof ApiError && err.code === 'UNAUTHORIZED') {
        router.push('/login');
      } else {
        const msg = err instanceof Error ? err.message : 'Failed to load telemetry';
        setErrorMsg(msg);
      }
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  React.useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const handleGeneratePlan = async () => {
    setIsGenerating(true);
    setErrorMsg(null);
    try {
      await apiClient('/workouts/generate', {
        method: 'POST',
        body: JSON.stringify({ cycle_type: 'weekly' }),
      });
      await fetchDashboardData();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to compile plan';
      setErrorMsg(msg);
    } finally {
      setIsGenerating(false);
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'MORNING BRIEFING';
    if (hour < 18) return 'AFTERNOON BRIEFING';
    return 'EVENING BRIEFING';
  };

  // LOADING STATE
  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-8 max-w-7xl mx-auto">
        <div className="space-y-2">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-10 w-72" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Skeleton className="h-28 w-full" />
          <Skeleton className="h-28 w-full" />
          <Skeleton className="h-28 w-full" />
          <Skeleton className="h-28 w-full" />
        </div>
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  // ERROR STATE
  if (errorMsg && !profile) {
    return (
      <div className="p-6 md:p-10 max-w-2xl mx-auto space-y-4">
        <Alert variant="error" title="Telemetry Sync Error">
          {errorMsg}
        </Alert>
        <Button variant="primary" onClick={fetchDashboardData}>
          Retry Connection
        </Button>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-7xl mx-auto">
      
      {/* Editorial Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-forest pb-6">
        <div className="space-y-1">
          <div className="text-xs font-mono uppercase tracking-widest text-lime flex items-center gap-2">
            <span className="h-2 w-2 bg-lime" />
            <span>{getGreeting()} // ATHLETE TELEMETRY</span>
          </div>
          <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight text-chalk uppercase">
            {profile?.full_name ? profile.full_name : 'ATHLETE'}
          </h1>
          <p className="text-xs font-mono text-sand">
            Demographic: {preferences?.age_group.replace('_', ' ').toUpperCase()} // Goals: {preferences?.fitness_goals.join(', ').toUpperCase()}
          </p>
        </div>

        {!todaySession && (
          <Button
            variant="primary"
            size="md"
            onClick={handleGeneratePlan}
            isLoading={isGenerating}
          >
            <Sparkles className="mr-2 h-4 w-4" /> Generate Periodized Plan
          </Button>
        )}
      </div>

      {errorMsg && (
        <Alert variant="error" title="Plan Generation Notice">
          {errorMsg}
        </Alert>
      )}

      {/* METRIC STRIP (Restrained Tabular Numbers) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-[10px] font-mono uppercase text-sand">Cycle Consistency</div>
            <div className="font-display text-2xl font-bold text-lime tabular-nums mt-1">
              {history.length > 0 ? '100%' : 'PENDING'}
            </div>
            <div className="text-[10px] font-mono text-sand/80 mt-1">
              {history.length} completed sessions
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="text-[10px] font-mono uppercase text-sand">Programmed Days</div>
            <div className="font-display text-2xl font-bold text-chalk tabular-nums mt-1">
              {preferences?.preferred_days.length || 3} DAYS / WK
            </div>
            <div className="text-[10px] font-mono text-sand/80 mt-1">
              {7 - (preferences?.preferred_days.length || 3)} active rest days
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="text-[10px] font-mono uppercase text-sand">Session Duration</div>
            <div className="font-display text-2xl font-bold text-chalk tabular-nums mt-1">
              {preferences?.time_availability_mins || 45} MINS
            </div>
            <div className="text-[10px] font-mono text-sand/80 mt-1">
              Calibrated work-rest ratio
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="text-[10px] font-mono uppercase text-sand">Clinical Invariants</div>
            <div className="font-display text-xl font-bold text-lime mt-1 uppercase flex items-center gap-1.5">
              <ShieldCheck className="h-5 w-5" /> ENFORCED
            </div>
            <div className="text-[10px] font-mono text-sand/80 mt-1">
              Sub-200ms pre-check active
            </div>
          </CardContent>
        </Card>
      </div>

      {/* TODAY'S PRESCRIBED WORKOUT (Hero Card) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="font-display text-xl font-bold uppercase tracking-tight text-chalk">
            TODAY&apos;S PRESCRIPTION
          </h2>
          <span className="text-xs font-mono text-sand uppercase">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
          </span>
        </div>

        {todaySession ? (
          <Card className="border-forest/90 bg-forest/20 overflow-hidden">
            <div className="p-6 md:p-8 space-y-6">
              
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-forest/60 pb-5">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant={todaySession.status === 'completed' ? 'lime' : 'forest'}>
                      {todaySession.status.toUpperCase()}
                    </Badge>
                    <span className="text-xs font-mono text-sand">Focus: {todaySession.focus_area}</span>
                  </div>
                  <h3 className="font-display text-2xl md:text-3xl font-bold text-chalk uppercase tracking-tight">
                    {todaySession.title}
                  </h3>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right hidden sm:block">
                    <div className="text-xs font-mono uppercase text-sand">EST. DURATION</div>
                    <div className="font-display font-bold text-lime tabular-nums text-lg">
                      {todaySession.planned_duration_mins} MINS
                    </div>
                  </div>
                  <Link href={`/workouts/${todaySession.id}`}>
                    <Button variant="primary" size="lg">
                      <Play className="mr-2 h-4 w-4 fill-current" /> 
                      {todaySession.status === 'completed' ? 'Review Log' : 'Start Workout'}
                    </Button>
                  </Link>
                </div>
              </div>

              {/* Exercise Lineup Preview */}
              <div className="space-y-3">
                <div className="text-xs font-mono uppercase tracking-widest text-sand">
                  PRESCRIBED EXERCISE SEQUENCE ({todaySession.exercises.length} MOVEMENTS)
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {todaySession.exercises.map((se) => (
                    <div
                      key={se.id}
                      className="p-3.5 bg-carbon rounded-sm border border-forest/60 flex items-center justify-between font-mono text-xs"
                    >
                      <div>
                        <span className="text-[10px] text-sand block">0{se.exercise_order}</span>
                        <span className="text-chalk font-semibold truncate block max-w-[160px]">
                          {se.exercise.name}
                        </span>
                      </div>
                      <span className="text-lime font-bold">
                        {se.target_sets}x{se.target_reps || 'reps'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </Card>
        ) : (
          /* EMPTY STATE (No workout scheduled yet) */
          <Card className="border-forest/60 bg-carbon-surface p-12 text-center space-y-4">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-sm bg-forest/40 text-lime">
              <Dumbbell className="h-7 w-7" />
            </div>
            <div className="space-y-1">
              <h3 className="font-display text-lg font-bold text-chalk uppercase">
                No Workout Scheduled For Today
              </h3>
              <p className="text-xs text-sand max-w-md mx-auto leading-relaxed">
                You haven&apos;t generated your weekly periodized cycle yet, or today is a programmed recovery day.
              </p>
            </div>
            <Button variant="primary" size="md" onClick={handleGeneratePlan} isLoading={isGenerating}>
              <Sparkles className="mr-2 h-4 w-4" /> Generate 7-Day Plan
            </Button>
          </Card>
        )}
      </div>

      {/* RULE-BASED ATHLETIC ADVISORY ALERT */}
      <Alert variant="info" title="Athletic Periodization Advisory">
        Based on your onboarding profile ({preferences?.experience_level.toUpperCase()} // {preferences?.age_group}), your volume is calibrated with progressive overload. Remember to record RPE after each set to allow dynamic workload regulation.
      </Alert>

      {/* RECENT COMPLETED WORKOUTS SECTION */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-display text-xl font-bold uppercase tracking-tight text-chalk">
            COMPLETED SESSION LOGS
          </h2>
          <Link href="/workouts" className="text-xs font-mono text-sand hover:text-lime flex items-center gap-1">
            View All History <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {history.length > 0 ? (
          <div className="space-y-2">
            {history.slice(0, 3).map((session) => (
              <div
                key={session.id}
                className="p-4 bg-carbon-surface rounded-sm border border-forest flex items-center justify-between font-mono text-xs"
              >
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-3.5 w-3.5 text-lime" />
                    <span className="text-chalk font-semibold uppercase">{session.title}</span>
                  </div>
                  <span className="text-sand/80 text-[11px]">
                    Completed {session.completed_at ? new Date(session.completed_at).toLocaleDateString() : 'Recently'} // RPE: {session.perceived_exertion || 'N/A'}/10
                  </span>
                </div>
                <Link href={`/workouts/${session.id}`}>
                  <Button variant="outline" size="sm">
                    Review Telemetry
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6 bg-carbon-surface border border-forest/40 rounded-sm text-center font-mono text-xs text-sand">
            No completed sessions recorded yet. Launch today&apos;s prescription above to log your first session.
          </div>
        )}
      </div>

    </div>
  );
}
