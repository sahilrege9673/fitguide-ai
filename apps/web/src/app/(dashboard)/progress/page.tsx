'use client';

import * as React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert } from '@/components/ui/alert';
import { apiClient, ApiError } from '@/lib/api/client';
import { createClient } from '@/lib/supabase/client';
import {
  TrendingUp,
  Download,
  Calendar,
  Flame,
  Dumbbell,
  Clock,
  Sparkles,
  BarChart3,
  Layers,
  ArrowUpRight,
  RefreshCw,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

interface DailyActivity {
  date: string;
  day_name: string;
  completed: boolean;
  workout_title: string | null;
  active_mins: number;
  volume_kg: number;
  sets_count: number;
}

interface MuscleGroupVolume {
  muscle_group: string;
  display_name: string;
  sets: number;
  volume_kg: number;
  percentage: number;
}

interface ProgressSummary {
  timeframe: string;
  start_date: string;
  end_date: string;
  consistency_percentage: number;
  completed_workouts: number;
  scheduled_workouts: number;
  total_volume_kg: number;
  total_active_mins: number;
  total_reps: number;
  total_sets: number;
  streak_days: number;
  muscle_group_distribution: MuscleGroupVolume[];
  daily_activity: DailyActivity[];
  ai_insights: string;
  generated_at: string;
}

const TIMEFRAMES = [
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
  { label: '90D', value: '90d' },
  { label: 'ALL', value: 'all' },
];

export default function ProgressPage() {
  const [timeframe, setTimeframe] = React.useState<string>('30d');
  const [summary, setSummary] = React.useState<ProgressSummary | null>(null);
  const [isLoading, setIsLoading] = React.useState<boolean>(true);
  const [isDownloadingPdf, setIsDownloadingPdf] = React.useState<boolean>(false);
  const [error, setError] = React.useState<string | null>(null);

  const fetchSummary = React.useCallback(async (tf: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiClient<ProgressSummary>(`/progress/summary?timeframe=${tf}`);
      setSummary(data);
    } catch (err) {
      console.error('Failed to load progress summary:', err);
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Unable to load progress telemetry. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  React.useEffect(() => {
    fetchSummary(timeframe);
  }, [timeframe, fetchSummary]);

  const handleDownloadPdf = async () => {
    setIsDownloadingPdf(true);
    try {
      const supabase = createClient();
      const { data: { session } } = await supabase.auth.getSession();
      const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';
      const url = `${apiBase}/progress/report/pdf?timeframe=${timeframe}`;

      const res = await fetch(url, {
        headers: {
          Authorization: `Bearer ${session?.access_token || ''}`,
        },
      });

      if (!res.ok) {
        throw new Error('Failed to download activity report.');
      }

      const blob = await res.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `feedguide-performance-report-${timeframe}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err) {
      console.error('PDF download error:', err);
      alert('Failed to generate PDF activity report. Please check connection and try again.');
    } finally {
      setIsDownloadingPdf(false);
    }
  };

  // Find max daily volume for proportional chart bars
  const maxDailyVolume = React.useMemo(() => {
    if (!summary || !summary.daily_activity.length) return 1;
    const maxVal = Math.max(...summary.daily_activity.map(d => d.volume_kg), 0);
    return maxVal > 0 ? maxVal : 1;
  }, [summary]);

  return (
    <div className="space-y-8 pb-16">
      
      {/* 1. EDITORIAL HEADER & ACTION BAR */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-forest pb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="h-2 w-2 bg-lime" />
            <span className="font-mono text-xs uppercase tracking-widest text-lime">
              TELEMETRY & ANALYTICS
            </span>
          </div>
          <h1 className="font-display text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-chalk uppercase">
            TRAINING PROGRESS
          </h1>
          <p className="font-sans text-sm text-sand mt-1 max-w-2xl">
            Consistency scoring, accumulated mechanical workload, anatomical volume balance, and grounded coach feedback.
          </p>
        </div>

        {/* Action Controls: Timeframe Pills & PDF Export */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Timeframe Selectors */}
          <div className="flex bg-forest/40 p-1 rounded-sm border border-forest">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf.value}
                onClick={() => setTimeframe(tf.value)}
                disabled={isLoading}
                className={`px-3 py-1.5 font-mono text-xs uppercase tracking-wider rounded-none transition-colors duration-fast ${
                  timeframe === tf.value
                    ? 'bg-lime text-carbon font-bold'
                    : 'text-sand hover:text-chalk'
                }`}
              >
                {tf.label}
              </button>
            ))}
          </div>

          {/* Download PDF Activity Report */}
          <Button
            onClick={handleDownloadPdf}
            disabled={isDownloadingPdf || isLoading || !summary}
            className="bg-carbon border border-lime text-lime hover:bg-lime hover:text-carbon font-mono text-xs uppercase tracking-wider h-9 px-4 rounded-none transition-all duration-fast flex items-center gap-2"
          >
            {isDownloadingPdf ? (
              <>
                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                <span>BUILDING PDF...</span>
              </>
            ) : (
              <>
                <Download className="h-3.5 w-3.5" />
                <span>EXPORT PDF REPORT</span>
              </>
            )}
          </Button>
        </div>
      </div>

      {/* ERROR STATE */}
      {error && (
        <Alert variant="error" className="rounded-none border-burnt bg-burnt/10 text-chalk">
          <div className="flex items-center gap-3">
            <AlertCircle className="h-5 w-5 text-burnt shrink-0" />
            <div className="flex-1">
              <p className="font-mono text-xs uppercase tracking-wider text-burnt font-bold">TELEMETRY ERROR</p>
              <p className="text-sm text-sand mt-0.5">{error}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => fetchSummary(timeframe)}
              className="rounded-none border-forest text-xs font-mono"
            >
              RETRY
            </Button>
          </div>
        </Alert>
      )}

      {/* SKELETON LOADING STATE */}
      {isLoading && !summary && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-28 bg-forest/30 border border-forest rounded-none" />
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Skeleton className="lg:col-span-2 h-80 bg-forest/30 border border-forest rounded-none" />
            <Skeleton className="h-80 bg-forest/30 border border-forest rounded-none" />
          </div>
          <Skeleton className="h-40 bg-forest/30 border border-forest rounded-none" />
        </div>
      )}

      {/* ACTIVE ANALYTICS DASHBOARD */}
      {summary && (
        <div className="space-y-8">
          
          {/* 2. EXECUTIVE KPI CARDS GRID */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            
            {/* KPI 1: Consistency Index */}
            <div className="bg-forest/30 border border-forest p-4 rounded-none flex flex-col justify-between">
              <div className="flex items-center justify-between text-sand">
                <span className="font-mono text-[10px] uppercase tracking-widest">CONSISTENCY</span>
                <CheckCircle2 className="h-4 w-4 text-lime" />
              </div>
              <div className="mt-3">
                <span className="font-display text-3xl lg:text-4xl font-bold tracking-tight text-chalk">
                  {summary.consistency_percentage}%
                </span>
                <div className="w-full bg-forest h-1 mt-2.5 rounded-none overflow-hidden">
                  <div
                    className="bg-lime h-full transition-all duration-500"
                    style={{ width: `${Math.min(100, summary.consistency_percentage)}%` }}
                  />
                </div>
              </div>
              <span className="font-mono text-[10px] text-sand mt-2">
                {summary.completed_workouts} of {summary.scheduled_workouts} scheduled
              </span>
            </div>

            {/* KPI 2: Completed Sessions */}
            <div className="bg-forest/30 border border-forest p-4 rounded-none flex flex-col justify-between">
              <div className="flex items-center justify-between text-sand">
                <span className="font-mono text-[10px] uppercase tracking-widest">SESSIONS COMPLETED</span>
                <Dumbbell className="h-4 w-4 text-lime" />
              </div>
              <div className="mt-3">
                <span className="font-display text-3xl lg:text-4xl font-bold tracking-tight text-chalk">
                  {summary.completed_workouts}
                </span>
                <span className="font-mono text-xs text-sand ml-1.5">BOUTS</span>
              </div>
              <span className="font-mono text-[10px] text-sand mt-2">
                {summary.total_sets} total working sets
              </span>
            </div>

            {/* KPI 3: Total Volume Load */}
            <div className="bg-forest/30 border border-forest p-4 rounded-none flex flex-col justify-between">
              <div className="flex items-center justify-between text-sand">
                <span className="font-mono text-[10px] uppercase tracking-widest">VOLUME LOAD</span>
                <BarChart3 className="h-4 w-4 text-lime" />
              </div>
              <div className="mt-3">
                <span className="font-display text-3xl lg:text-4xl font-bold tracking-tight text-lime">
                  {Math.round(summary.total_volume_kg).toLocaleString()}
                </span>
                <span className="font-mono text-xs text-sand ml-1.5">KG</span>
              </div>
              <span className="font-mono text-[10px] text-sand mt-2">
                {summary.total_reps.toLocaleString()} executed reps
              </span>
            </div>

            {/* KPI 4: Active Time */}
            <div className="bg-forest/30 border border-forest p-4 rounded-none flex flex-col justify-between">
              <div className="flex items-center justify-between text-sand">
                <span className="font-mono text-[10px] uppercase tracking-widest">TRAINING TIME</span>
                <Clock className="h-4 w-4 text-lime" />
              </div>
              <div className="mt-3">
                <span className="font-display text-3xl lg:text-4xl font-bold tracking-tight text-chalk">
                  {Math.round(summary.total_active_mins)}
                </span>
                <span className="font-mono text-xs text-sand ml-1.5">MINS</span>
              </div>
              <span className="font-mono text-[10px] text-sand mt-2">
                ~{(summary.total_active_mins / 60).toFixed(1)} hrs active stimulus
              </span>
            </div>

            {/* KPI 5: Current Streak */}
            <div className="bg-forest/30 border border-forest p-4 rounded-none flex flex-col justify-between col-span-2 md:col-span-1">
              <div className="flex items-center justify-between text-sand">
                <span className="font-mono text-[10px] uppercase tracking-widest">ACTIVE STREAK</span>
                <Flame className="h-4 w-4 text-burnt" />
              </div>
              <div className="mt-3">
                <span className="font-display text-3xl lg:text-4xl font-bold tracking-tight text-chalk">
                  {summary.streak_days}
                </span>
                <span className="font-mono text-xs text-sand ml-1.5">DAYS</span>
              </div>
              <span className="font-mono text-[10px] text-sand mt-2">
                Consecutive training cadence
              </span>
            </div>

          </div>

          {/* 3. VISUAL CHARTS SECTION */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* 3A. DAILY WORKLOAD & COMPLETION TIMELINE (2 cols) */}
            <Card className="lg:col-span-2 bg-forest/20 border-forest rounded-none p-6 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between border-b border-forest pb-4 mb-6">
                  <div>
                    <span className="font-mono text-[10px] uppercase tracking-widest text-lime">
                      WORKLOAD DISTRIBUTION
                    </span>
                    <h3 className="font-display text-xl font-bold tracking-tight text-chalk mt-0.5">
                      SESSION CADENCE & DAILY VOLUME
                    </h3>
                  </div>
                  <Badge variant="outline" className="border-forest text-sand font-mono text-[10px] rounded-none">
                    {summary.start_date} → {summary.end_date}
                  </Badge>
                </div>

                {/* Bar Chart Visualization */}
                <div className="h-56 flex items-end gap-2 pt-6 pb-2 border-b border-forest">
                  {summary.daily_activity.map((day) => {
                    const heightPercent = day.completed && day.volume_kg > 0
                      ? Math.max(15, Math.round((day.volume_kg / maxDailyVolume) * 100))
                      : day.completed
                      ? 25
                      : 4;

                    return (
                      <div
                        key={day.date}
                        className="flex-1 flex flex-col items-center justify-end h-full group relative"
                      >
                        {/* Tooltip on Hover */}
                        <div className="absolute -top-14 opacity-0 group-hover:opacity-100 transition-opacity duration-fast pointer-events-none z-20 bg-carbon border border-forest p-2 text-center whitespace-nowrap shadow-lg">
                          <p className="font-mono text-[10px] text-lime uppercase">{day.date} ({day.day_name})</p>
                          <p className="font-sans text-xs text-chalk font-bold">
                            {day.completed ? (day.workout_title || 'Session Completed') : 'Rest / Inactive'}
                          </p>
                          {day.completed && (
                            <p className="font-mono text-[10px] text-sand">
                              {day.volume_kg.toLocaleString()} kg · {day.active_mins}m · {day.sets_count} sets
                            </p>
                          )}
                        </div>

                        {/* Bar Pillar */}
                        <div
                          className={`w-full rounded-none transition-all duration-300 ${
                            day.completed
                              ? 'bg-lime group-hover:bg-chalk'
                              : 'bg-forest/50 hover:bg-forest'
                          }`}
                          style={{ height: `${heightPercent}%` }}
                        />
                      </div>
                    );
                  })}
                </div>

                {/* Day Labels Axis */}
                <div className="flex gap-2 pt-2">
                  {summary.daily_activity.map((day) => (
                    <div key={day.date} className="flex-1 text-center font-mono text-[10px] text-sand truncate">
                      {day.day_name}
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-6 pt-4 text-xs font-mono text-sand">
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 bg-lime" />
                  <span>COMPLETED WORKOUT</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 bg-forest" />
                  <span>SCHEDULED / REST DAY</span>
                </div>
              </div>
            </Card>

            {/* 3B. MUSCLE GROUP ANATOMICAL BREAKDOWN (1 col) */}
            <Card className="bg-forest/20 border-forest rounded-none p-6 flex flex-col justify-between">
              <div>
                <div className="border-b border-forest pb-4 mb-4">
                  <span className="font-mono text-[10px] uppercase tracking-widest text-lime">
                    ANATOMICAL BALANCE
                  </span>
                  <h3 className="font-display text-xl font-bold tracking-tight text-chalk mt-0.5">
                    MUSCLE VOLUME SPLIT
                  </h3>
                </div>

                {summary.muscle_group_distribution.length > 0 ? (
                  <div className="space-y-3.5 mt-4">
                    {summary.muscle_group_distribution.slice(0, 6).map((item) => (
                      <div key={item.muscle_group} className="space-y-1">
                        <div className="flex justify-between items-center text-xs">
                          <span className="font-sans font-medium text-chalk truncate max-w-[140px]">
                            {item.display_name}
                          </span>
                          <span className="font-mono text-sand text-[11px]">
                            {item.sets} sets · <span className="text-lime">{item.percentage}%</span>
                          </span>
                        </div>
                        {/* Progress meter bar */}
                        <div className="w-full bg-forest h-1.5 rounded-none overflow-hidden">
                          <div
                            className="bg-lime h-full transition-all duration-500"
                            style={{ width: `${item.percentage}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-12 text-center text-sand space-y-2">
                    <Layers className="h-8 w-8 mx-auto text-forest" />
                    <p className="font-mono text-xs uppercase tracking-wider">No logged muscle sets</p>
                    <p className="text-xs max-w-xs mx-auto">
                      Execute and log exercises in active workouts to render anatomical volume distribution.
                    </p>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-forest">
                <span className="font-mono text-[10px] text-sand uppercase">
                  Calibrated to ACSM/NSCA progressive overload guidelines
                </span>
              </div>
            </Card>

          </div>

          {/* 4. GROUNDED AI ATHLETIC COACH ANALYSIS */}
          <Card className="bg-forest/30 border-forest border-l-4 border-l-lime rounded-none p-6 relative overflow-hidden">
            <div className="flex items-start gap-4">
              <div className="h-10 w-10 bg-lime/10 border border-lime flex items-center justify-center shrink-0">
                <Sparkles className="h-5 w-5 text-lime" />
              </div>
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs uppercase tracking-widest text-lime font-bold">
                    AI COACH BIOMECHANICAL AUDIT
                  </span>
                  <Badge variant="outline" className="border-forest text-sand text-[9px] font-mono rounded-none">
                    GROUNDED INSIGHTS
                  </Badge>
                </div>

                <div className="text-sm font-sans text-chalk leading-relaxed whitespace-pre-line space-y-2">
                  {summary.ai_insights}
                </div>

                <div className="pt-3 flex items-center gap-4 text-xs font-mono text-sand">
                  <span>LAST EVALUATED: {new Date(summary.generated_at).toLocaleDateString()}</span>
                  <span>·</span>
                  <Link href="/assistant" className="text-lime hover:underline flex items-center gap-1">
                    <span>DISCUSS WITH AI ASSISTANT</span>
                    <ArrowUpRight className="h-3 w-3" />
                  </Link>
                </div>
              </div>
            </div>
          </Card>

          {/* 5. EMPTY STATE ASSISTANCE IF 0 WORKOUTS COMPLETED */}
          {summary.completed_workouts === 0 && (
            <div className="border border-forest bg-forest/10 p-6 rounded-none flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h4 className="font-display text-lg font-bold text-chalk uppercase">
                  READY TO RECORD YOUR FIRST SESSION?
                </h4>
                <p className="text-sm text-sand mt-0.5">
                  Complete today&apos;s scheduled routine to populate active volume load and start your consistency streak.
                </p>
              </div>
              <Link href="/workouts">
                <Button className="bg-lime text-carbon hover:bg-chalk font-mono text-xs uppercase tracking-wider font-bold h-10 px-5 rounded-none shrink-0">
                  START WORKOUT
                </Button>
              </Link>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
