'use client';

import * as React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient } from '@/lib/api/client';
import { Dumbbell, Play, CheckCircle2, Sparkles, Clock, Calendar, ArrowRight } from 'lucide-react';

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
      name: string;
    };
  }>;
  feedback?: {
    energy_rating: number;
    difficulty_rating: number;
    soreness_level: string;
  };
}

export default function WorkoutsHubPage() {
  const [todaySession, setTodaySession] = React.useState<WorkoutSession | null>(null);
  const [history, setHistory] = React.useState<WorkoutSession[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [isGenerating, setIsGenerating] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const loadWorkouts = React.useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const today = await apiClient<WorkoutSession | null>('/workouts/today').catch(() => null);
      setTodaySession(today);

      const hist = await apiClient<WorkoutSession[]>('/workouts/history').catch(() => []);
      setHistory(hist);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch workouts';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  }, []);

  React.useEffect(() => {
    loadWorkouts();
  }, [loadWorkouts]);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setErrorMsg(null);
    try {
      await apiClient('/workouts/generate', {
        method: 'POST',
        body: JSON.stringify({ cycle_type: 'weekly' }),
      });
      await loadWorkouts();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Generation failed';
      setErrorMsg(msg);
    } finally {
      setIsGenerating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-6 max-w-7xl mx-auto">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-48 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-7xl mx-auto">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-forest pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Badge variant="lime">PERIODIZED CYCLES</Badge>
            <span className="text-xs font-mono uppercase tracking-widest text-sand">
              TRAINING MANAGEMENT
            </span>
          </div>
          <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight text-chalk uppercase">
            MY WORKOUTS
          </h1>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleGenerate}
          isLoading={isGenerating}
        >
          <Sparkles className="mr-2 h-4 w-4" /> Re-generate Cycle
        </Button>
      </div>

      {errorMsg && (
        <Alert variant="error" title="Notice">
          {errorMsg}
        </Alert>
      )}

      {/* TODAY'S ACTIVE WORKOUT */}
      <div className="space-y-3">
        <h2 className="font-display text-xl font-bold uppercase tracking-tight text-chalk">
          ACTIVE SESSION
        </h2>

        {todaySession ? (
          <Card className="border-forest/90 bg-forest/20">
            <div className="p-6 md:p-8 space-y-6">
              <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Badge variant={todaySession.status === 'completed' ? 'lime' : 'forest'}>
                      {todaySession.status.toUpperCase()}
                    </Badge>
                    <span className="text-xs font-mono text-sand">Focus: {todaySession.focus_area}</span>
                  </div>
                  <h3 className="font-display text-2xl font-bold uppercase text-chalk">
                    {todaySession.title}
                  </h3>
                </div>

                <Link href={`/workouts/${todaySession.id}`}>
                  <Button variant="primary" size="lg">
                    <Play className="mr-2 h-4 w-4 fill-current" />
                    {todaySession.status === 'completed' ? 'Review Session' : 'Enter Player'}
                  </Button>
                </Link>
              </div>

              {/* Exercise count & time info */}
              <div className="flex items-center gap-6 pt-4 border-t border-forest/60 text-xs font-mono text-sand">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-lime" />
                  <span>{todaySession.planned_duration_mins} Minutes Target</span>
                </div>
                <div className="flex items-center gap-2">
                  <Dumbbell className="h-4 w-4 text-lime" />
                  <span>{todaySession.exercises.length} Prescribed Movements</span>
                </div>
              </div>
            </div>
          </Card>
        ) : (
          <Card className="p-8 text-center border-forest bg-carbon-surface space-y-3">
            <p className="text-xs text-sand font-mono">No active session programmed for today.</p>
            <Button variant="primary" size="sm" onClick={handleGenerate} isLoading={isGenerating}>
              Generate 7-Day Cycle
            </Button>
          </Card>
        )}
      </div>

      {/* WORKOUT LOG HISTORY */}
      <div className="space-y-4">
        <h2 className="font-display text-xl font-bold uppercase tracking-tight text-chalk">
          COMPLETED WORKOUT HISTORY ({history.length})
        </h2>

        {history.length > 0 ? (
          <div className="space-y-3">
            {history.map((s) => (
              <Card key={s.id} className="p-5 border-forest hover:border-sand/40 transition-colors duration-fast">
                <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-lime" />
                      <h4 className="font-display font-semibold text-base text-chalk uppercase tracking-tight">
                        {s.title}
                      </h4>
                      <Badge variant="lime">COMPLETED</Badge>
                    </div>
                    <div className="flex flex-wrap gap-4 text-xs font-mono text-sand pt-1">
                      <span>Date: {s.completed_at ? new Date(s.completed_at).toLocaleDateString() : 'N/A'}</span>
                      <span>Focus: {s.focus_area}</span>
                      {s.perceived_exertion && <span>RPE: {s.perceived_exertion}/10</span>}
                      {s.feedback && <span>Energy: {s.feedback.energy_rating}/5</span>}
                    </div>
                  </div>

                  <Link href={`/workouts/${s.id}`}>
                    <Button variant="outline" size="sm">
                      View Telemetry <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
                    </Button>
                  </Link>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="p-10 text-center border-forest/60 bg-carbon-surface space-y-2">
            <p className="text-xs text-sand font-mono">
              No completed sessions logged yet. When you complete a workout in the player, your telemetry will record here.
            </p>
          </Card>
        )}
      </div>

    </div>
  );
}
