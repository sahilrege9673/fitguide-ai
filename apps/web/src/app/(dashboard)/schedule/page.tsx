'use client';

import * as React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient } from '@/lib/api/client';
import { Calendar, Play, CheckCircle2, Moon, Clock, ArrowRight, RefreshCw } from 'lucide-react';

interface ScheduleEntry {
  id: string;
  session_id?: string;
  scheduled_date: string;
  entry_type: string;
  title: string;
  is_rest_day: boolean;
  is_completed: boolean;
}

export default function SchedulePage() {
  const [entries, setEntries] = React.useState<ScheduleEntry[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  // Rescheduling state
  const [reschedulingEntry, setReschedulingEntry] = React.useState<ScheduleEntry | null>(null);
  const [newDate, setNewDate] = React.useState('');
  const [isRescheduling, setIsRescheduling] = React.useState(false);

  const fetchSchedule = React.useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await apiClient<ScheduleEntry[]>('/schedule');
      setEntries(res);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load schedule';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  }, []);

  React.useEffect(() => {
    fetchSchedule();
  }, [fetchSchedule]);

  const handleRescheduleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reschedulingEntry || !newDate) return;

    setIsRescheduling(true);
    try {
      await apiClient(`/schedule/${reschedulingEntry.id}/reschedule`, {
        method: 'PATCH',
        body: JSON.stringify({ new_date: newDate }),
      });
      setReschedulingEntry(null);
      await fetchSchedule();
    } catch (err: unknown) {
      console.error('Failed to reschedule:', err);
    } finally {
      setIsRescheduling(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-6 max-w-7xl mx-auto">
        <Skeleton className="h-8 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-7 gap-3">
          {Array.from({ length: 7 }).map((_, i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-7xl mx-auto">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-forest pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Badge variant="lime">CALENDAR TELEMETRY</Badge>
            <span className="text-xs font-mono uppercase tracking-widest text-sand">
              WEEKLY PERIODIZATION
            </span>
          </div>
          <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight text-chalk uppercase">
            MY SCHEDULE
          </h1>
        </div>

        <Link href="/workouts">
          <Button variant="outline" size="sm">
            View Current Active Plan
          </Button>
        </Link>
      </div>

      {errorMsg && (
        <Alert variant="error" title="Notice">
          {errorMsg}
        </Alert>
      )}

      {/* 7-DAY CALENDAR TILES */}
      {entries.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 gap-3">
          {entries.map((entry) => {
            const entryDate = new Date(entry.scheduled_date);
            const dayName = entryDate.toLocaleDateString('en-US', { weekday: 'short' });
            const dayNum = entryDate.getDate();
            const monthName = entryDate.toLocaleDateString('en-US', { month: 'short' });

            return (
              <Card
                key={entry.id}
                className={`flex flex-col justify-between p-4 min-h-[220px] transition-colors duration-fast ${
                  entry.is_completed
                    ? 'border-lime/40 bg-forest/20'
                    : entry.is_rest_day
                    ? 'border-forest/60 bg-carbon-surface/40'
                    : 'border-forest bg-carbon-surface hover:border-lime/60'
                }`}
              >
                <div className="space-y-3">
                  {/* Date Header */}
                  <div className="flex items-center justify-between border-b border-forest/60 pb-2 font-mono text-xs">
                    <span className="font-bold text-chalk uppercase">{dayName}</span>
                    <span className="text-sand">{monthName} {dayNum}</span>
                  </div>

                  {/* Badge & Title */}
                  <div className="space-y-1.5">
                    {entry.is_completed ? (
                      <Badge variant="lime">COMPLETED</Badge>
                    ) : entry.is_rest_day ? (
                      <Badge variant="sand">REST / RECOVERY</Badge>
                    ) : (
                      <Badge variant="forest">SCHEDULED</Badge>
                    )}

                    <h4 className="font-display font-semibold text-sm text-chalk uppercase line-clamp-2 mt-1">
                      {entry.title}
                    </h4>
                  </div>
                </div>

                {/* Bottom Actions */}
                <div className="pt-3 border-t border-forest/40 flex flex-col gap-2">
                  {!entry.is_rest_day && entry.session_id && (
                    <Link href={`/workouts/${entry.session_id}`}>
                      <Button variant={entry.is_completed ? 'outline' : 'primary'} size="sm" className="w-full text-[11px]">
                        {entry.is_completed ? 'View Telemetry' : 'Launch Session'}
                      </Button>
                    </Link>
                  )}

                  {!entry.is_completed && !entry.is_rest_day && (
                    <button
                      onClick={() => {
                        setReschedulingEntry(entry);
                        setNewDate(entry.scheduled_date);
                      }}
                      className="text-[10px] font-mono text-sand hover:text-chalk text-center flex items-center justify-center gap-1"
                    >
                      <RefreshCw className="h-3 w-3" /> Reschedule
                    </button>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="p-12 text-center border-forest bg-carbon-surface space-y-4">
          <Calendar className="h-8 w-8 text-sand mx-auto" />
          <h3 className="font-display font-bold text-lg text-chalk uppercase">
            No Active Schedule Found
          </h3>
          <p className="text-xs text-sand font-mono max-w-sm mx-auto">
            Generate your weekly workout cycle from the dashboard to populate your periodized training calendar.
          </p>
          <Link href="/dashboard">
            <Button variant="primary" size="sm">
              Go to Dashboard
            </Button>
          </Link>
        </Card>
      )}

      {/* RESCHEDULE MODAL */}
      {reschedulingEntry && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-carbon/80 backdrop-blur-sm p-4">
          <Card className="w-full max-w-md border-forest bg-carbon space-y-4">
            <CardHeader>
              <CardTitle>Reschedule Workout</CardTitle>
              <CardDescription>
                Shift &quot;{reschedulingEntry.title}&quot; to a new calendar date.
              </CardDescription>
            </CardHeader>
            <form onSubmit={handleRescheduleSubmit}>
              <CardContent className="space-y-3 font-mono text-xs">
                <label className="text-sand uppercase block">Select New Date</label>
                <Input
                  type="date"
                  value={newDate}
                  onChange={(e) => setNewDate(e.target.value)}
                  required
                />
              </CardContent>
              <div className="p-6 pt-0 border-t border-forest/60 flex items-center justify-between">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setReschedulingEntry(null)}
                  disabled={isRescheduling}
                >
                  Cancel
                </Button>
                <Button type="submit" variant="primary" isLoading={isRescheduling}>
                  Confirm Reschedule
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}

    </div>
  );
}
