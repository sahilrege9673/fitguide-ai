'use client';

import * as React from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient, ApiError } from '@/lib/api/client';
import { 
  ArrowLeft, 
  Play, 
  Pause, 
  RotateCcw, 
  CheckCircle2, 
  Clock, 
  RefreshCw, 
  Save, 
  Flame, 
  Check,
  ChevronDown
} from 'lucide-react';

interface ExerciseLog {
  id: string;
  set_number: number;
  weight_kg: number;
  reps_performed?: number;
  rpe?: number;
}

interface SessionExercise {
  id: string;
  exercise_order: number;
  exercise_id: string;
  target_sets: number;
  target_reps?: number;
  target_rest_secs: number;
  is_completed: boolean;
  exercise: {
    id: string;
    name: string;
    slug: string;
    category: string;
    primary_muscles: string[];
    instructions: string;
  };
  logs: ExerciseLog[];
}

interface WorkoutSessionDetail {
  id: string;
  title: string;
  focus_area: string;
  planned_duration_mins: number;
  status: string;
  perceived_exertion?: number;
  notes?: string;
  exercises: SessionExercise[];
}

export default function WorkoutPlayerPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params?.id as string;

  const [session, setSession] = React.useState<WorkoutSessionDetail | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  // Active inputs for logging sets (keyed by session_exercise_id)
  const [inputs, setInputs] = React.useState<Record<string, { weight: string; reps: string; rpe: string }>>({});
  const [isLoggingSet, setIsLoggingSet] = React.useState<string | null>(null);

  // Rest Timer State
  const [restTimerSeconds, setRestTimerSeconds] = React.useState(60);
  const [isTimerRunning, setIsTimerRunning] = React.useState(false);

  // Finish Workout Modal
  const [showFinishModal, setShowFinishModal] = React.useState(false);
  const [perceivedExertion, setPerceivedExertion] = React.useState(7);
  const [energyRating, setEnergyRating] = React.useState(4);
  const [difficultyRating, setDifficultyRating] = React.useState(4);
  const [sorenessLevel, setSorenessLevel] = React.useState('moderate');
  const [userComment, setUserComment] = React.useState('');
  const [isCompleting, setIsCompleting] = React.useState(false);

  // Swapping State
  const [swappingExerciseId, setSwappingExerciseId] = React.useState<string | null>(null);

  const fetchSession = React.useCallback(async () => {
    if (!sessionId) return;
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await apiClient<WorkoutSessionDetail>(`/workouts/sessions/${sessionId}`);
      setSession(res);

      // Prepopulate default inputs
      const initInputs: Record<string, { weight: string; reps: string; rpe: string }> = {};
      res.exercises.forEach((se) => {
        initInputs[se.id] = {
          weight: '60',
          reps: se.target_reps ? String(se.target_reps) : '10',
          rpe: '8',
        };
      });
      setInputs(initInputs);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load session player';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  React.useEffect(() => {
    fetchSession();
  }, [fetchSession]);

  // Timer Tick
  React.useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (isTimerRunning && restTimerSeconds > 0) {
      interval = setInterval(() => {
        setRestTimerSeconds((prev) => prev - 1);
      }, 1000);
    } else if (restTimerSeconds === 0) {
      setIsTimerRunning(false);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isTimerRunning, restTimerSeconds]);

  const handleStartSession = async () => {
    try {
      const res = await apiClient<WorkoutSessionDetail>(`/workouts/sessions/${sessionId}/start`, {
        method: 'POST',
      });
      setSession(res);
    } catch (err: unknown) {
      console.error('Failed to start session:', err);
    }
  };

  const handleLogSet = async (sessionExerciseId: string) => {
    const input = inputs[sessionExerciseId];
    if (!input) return;

    setIsLoggingSet(sessionExerciseId);
    setErrorMsg(null);

    const se = session?.exercises.find((e) => e.id === sessionExerciseId);
    const nextSetNumber = (se?.logs.length || 0) + 1;

    try {
      await apiClient(`/workouts/sessions/${sessionId}/log-exercise`, {
        method: 'POST',
        body: JSON.stringify({
          session_exercise_id: sessionExerciseId,
          set_number: nextSetNumber,
          weight_kg: parseFloat(input.weight) || 0,
          reps_performed: parseInt(input.reps) || 10,
          rpe: parseInt(input.rpe) || 8,
        }),
      });

      // Automatically start rest timer
      setRestTimerSeconds(se?.target_rest_secs || 60);
      setIsTimerRunning(true);

      await fetchSession();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to record set';
      setErrorMsg(msg);
    } finally {
      setIsLoggingSet(null);
    }
  };

  const handleSwapExercise = async (exerciseId: string) => {
    setSwappingExerciseId(exerciseId);
    setErrorMsg(null);
    try {
      await apiClient(`/workouts/sessions/${sessionId}/exercises/${exerciseId}/swap`, {
        method: 'POST',
        body: JSON.stringify({ reason: 'joint_discomfort' }),
      });
      await fetchSession();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Swap failed';
      setErrorMsg(msg);
    } finally {
      setSwappingExerciseId(null);
    }
  };

  const handleCompleteSession = async () => {
    setIsCompleting(true);
    setErrorMsg(null);
    try {
      await apiClient(`/workouts/sessions/${sessionId}/complete`, {
        method: 'POST',
        body: JSON.stringify({
          perceived_exertion: perceivedExertion,
          notes: userComment,
          feedback: {
            energy_rating: energyRating,
            difficulty_rating: difficultyRating,
            soreness_level: sorenessLevel,
            user_comment: userComment,
          },
        }),
      });

      router.push('/workouts');
      router.refresh();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to complete session';
      setErrorMsg(msg);
      setIsCompleting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-6 max-w-4xl mx-auto">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-72 w-full" />
      </div>
    );
  }

  if (errorMsg && !session) {
    return (
      <div className="p-6 md:p-10 max-w-xl mx-auto space-y-4">
        <Alert variant="error" title="Player Sync Notice">
          {errorMsg}
        </Alert>
        <Link href="/workouts">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" /> Return to Workouts
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-5xl mx-auto">
      
      {/* Top Bar with Navigation & Actions */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-forest pb-6">
        <div>
          <Link href="/workouts" className="inline-flex items-center text-xs font-mono uppercase tracking-widest text-sand hover:text-lime mb-2">
            <ArrowLeft className="mr-1.5 h-3.5 w-3.5" /> Back to My Workouts
          </Link>
          <div className="flex items-center gap-2">
            <Badge variant={session?.status === 'completed' ? 'lime' : 'forest'}>
              {session?.status.toUpperCase()}
            </Badge>
            <span className="text-xs font-mono text-sand">Focus: {session?.focus_area}</span>
          </div>
          <h1 className="font-display text-2xl sm:text-4xl font-bold tracking-tight text-chalk uppercase mt-1">
            {session?.title}
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {session?.status === 'scheduled' && (
            <Button variant="primary" onClick={handleStartSession}>
              <Play className="mr-2 h-4 w-4 fill-current" /> Begin Workout
            </Button>
          )}
          {session?.status === 'in_progress' && (
            <Button variant="primary" onClick={() => setShowFinishModal(true)}>
              <CheckCircle2 className="mr-2 h-4 w-4" /> Finish Session
            </Button>
          )}
        </div>
      </div>

      {errorMsg && (
        <Alert variant="error" title="Alert">
          {errorMsg}
        </Alert>
      )}

      {/* REST TIMER HUD */}
      <div className="bg-carbon-surface border border-forest p-4 rounded-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Clock className="h-5 w-5 text-lime" />
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-sand">INTER-SET REST TIMER</div>
            <div className="font-display text-3xl font-bold text-lime tabular-nums tracking-tight">
              {Math.floor(restTimerSeconds / 60)}:{(restTimerSeconds % 60).toString().padStart(2, '0')}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsTimerRunning(!isTimerRunning)}
          >
            {isTimerRunning ? <Pause className="h-3.5 w-3.5 mr-1" /> : <Play className="h-3.5 w-3.5 mr-1" />}
            {isTimerRunning ? 'Pause' : 'Start'}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setIsTimerRunning(false);
              setRestTimerSeconds(60);
            }}
          >
            <RotateCcw className="h-3.5 w-3.5 mr-1" /> 60s
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setIsTimerRunning(false);
              setRestTimerSeconds(90);
            }}
          >
            <RotateCcw className="h-3.5 w-3.5 mr-1" /> 90s
          </Button>
        </div>
      </div>

      {/* EXERCISE LIST */}
      <div className="space-y-6">
        {session?.exercises.map((se) => {
          const currentInput = inputs[se.id] || { weight: '60', reps: '10', rpe: '8' };
          const completedSets = se.logs.length;
          const isDone = completedSets >= se.target_sets;

          return (
            <Card key={se.id} className={`border-forest ${isDone ? 'border-lime/40 bg-forest/10' : ''}`}>
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-sand">0{se.exercise_order}.</span>
                    <CardTitle className="text-xl">{se.exercise.name}</CardTitle>
                    {isDone && <Check className="h-4 w-4 text-lime" />}
                  </div>
                  <CardDescription className="font-mono text-xs mt-1">
                    Target: {se.target_sets} sets &times; {se.target_reps || 10} reps // Rest: {se.target_rest_secs}s
                  </CardDescription>
                </div>

                <div className="flex items-center gap-2">
                  <Link href={`/exercises/${se.exercise.slug}`} target="_blank">
                    <Button variant="ghost" size="sm" className="text-xs font-mono">
                      Form Cues
                    </Button>
                  </Link>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleSwapExercise(se.exercise_id)}
                    isLoading={swappingExerciseId === se.exercise_id}
                    className="text-xs font-mono"
                  >
                    <RefreshCw className="h-3.5 w-3.5 mr-1" /> Swap
                  </Button>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Completed Sets Log Table */}
                {se.logs.length > 0 && (
                  <div className="border border-forest/60 rounded-sm overflow-hidden font-mono text-xs">
                    <div className="bg-carbon px-3 py-2 flex justify-between text-sand border-b border-forest/40">
                      <span>SET</span>
                      <span>LOAD (KG)</span>
                      <span>REPS</span>
                      <span>RPE</span>
                      <span>STATUS</span>
                    </div>
                    {se.logs.map((log) => (
                      <div key={log.id} className="px-3 py-2 flex justify-between border-b border-forest/20 text-chalk">
                        <span>Set {log.set_number}</span>
                        <span className="font-bold text-lime tabular-nums">{log.weight_kg} kg</span>
                        <span className="tabular-nums">{log.reps_performed} reps</span>
                        <span className="tabular-nums">RPE {log.rpe || 'N/A'}</span>
                        <span className="text-lime flex items-center gap-1 font-semibold">
                          <Check className="h-3 w-3" /> Recorded
                        </span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Input row for next set */}
                {session.status !== 'completed' && (
                  <div className="bg-carbon p-3.5 rounded-sm border border-forest grid grid-cols-2 sm:grid-cols-4 gap-3 items-end">
                    <div>
                      <label className="text-[10px] font-mono uppercase text-sand block mb-1">
                        Weight (KG)
                      </label>
                      <Input
                        type="number"
                        step="0.5"
                        value={currentInput.weight}
                        onChange={(e) =>
                          setInputs((prev) => ({
                            ...prev,
                            [se.id]: { ...currentInput, weight: e.target.value },
                          }))
                        }
                      />
                    </div>

                    <div>
                      <label className="text-[10px] font-mono uppercase text-sand block mb-1">
                        Reps Completed
                      </label>
                      <Input
                        type="number"
                        value={currentInput.reps}
                        onChange={(e) =>
                          setInputs((prev) => ({
                            ...prev,
                            [se.id]: { ...currentInput, reps: e.target.value },
                          }))
                        }
                      />
                    </div>

                    <div>
                      <label className="text-[10px] font-mono uppercase text-sand block mb-1">
                        Exertion (RPE 1-10)
                      </label>
                      <Input
                        type="number"
                        min="1"
                        max="10"
                        value={currentInput.rpe}
                        onChange={(e) =>
                          setInputs((prev) => ({
                            ...prev,
                            [se.id]: { ...currentInput, rpe: e.target.value },
                          }))
                        }
                      />
                    </div>

                    <Button
                      variant="primary"
                      onClick={() => handleLogSet(se.id)}
                      isLoading={isLoggingSet === se.id}
                      className="w-full"
                    >
                      <Save className="h-3.5 w-3.5 mr-1" /> Log Set {completedSets + 1}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* FINISH WORKOUT MODAL */}
      {showFinishModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-carbon/80 backdrop-blur-sm p-4">
          <Card className="w-full max-w-lg border-forest/90 bg-carbon space-y-4 shadow-2xl">
            <CardHeader>
              <CardTitle>Session Debrief &amp; Feedback</CardTitle>
              <CardDescription>
                Record your perceived exertion and recovery indicators to regulate upcoming training load.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-xs font-mono">
              <div className="space-y-1.5">
                <div className="flex justify-between">
                  <label className="text-sand uppercase">Session RPE (Perceived Exertion)</label>
                  <span className="text-lime font-bold text-sm">{perceivedExertion} / 10</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={perceivedExertion}
                  onChange={(e) => setPerceivedExertion(parseInt(e.target.value))}
                  className="w-full accent-[#C4E76B] bg-forest h-2 rounded-none cursor-pointer"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 pt-2">
                <div>
                  <label className="text-sand uppercase block mb-1">Energy Rating (1-5)</label>
                  <select
                    value={energyRating}
                    onChange={(e) => setEnergyRating(parseInt(e.target.value))}
                    className="w-full h-10 rounded-sm bg-carbon-surface border border-forest px-2 text-chalk"
                  >
                    <option value={5}>5 - High Energy</option>
                    <option value={4}>4 - Good</option>
                    <option value={3}>3 - Moderate</option>
                    <option value={2}>2 - Low</option>
                    <option value={1}>1 - Exhausted</option>
                  </select>
                </div>

                <div>
                  <label className="text-sand uppercase block mb-1">Muscle Soreness</label>
                  <select
                    value={sorenessLevel}
                    onChange={(e) => setSorenessLevel(e.target.value)}
                    className="w-full h-10 rounded-sm bg-carbon-surface border border-forest px-2 text-chalk"
                  >
                    <option value="none">None</option>
                    <option value="mild">Mild</option>
                    <option value="moderate">Moderate</option>
                    <option value="severe">High / Sore</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1 pt-2">
                <label className="text-sand uppercase block">Athlete Notes</label>
                <textarea
                  rows={3}
                  value={userComment}
                  onChange={(e) => setUserComment(e.target.value)}
                  placeholder="Notes on form, bar speed, or muscle pump..."
                  className="w-full p-2.5 rounded-sm bg-carbon-surface border border-forest text-chalk focus:outline-none focus:ring-2 focus:ring-lime"
                />
              </div>
            </CardContent>

            <div className="p-6 pt-0 border-t border-forest/60 flex items-center justify-between">
              <Button variant="ghost" onClick={() => setShowFinishModal(false)} disabled={isCompleting}>
                Cancel
              </Button>
              <Button variant="primary" onClick={handleCompleteSession} isLoading={isCompleting}>
                Save Telemetry &amp; Exit
              </Button>
            </div>
          </Card>
        </div>
      )}

    </div>
  );
}
