'use client';

import * as React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient, ApiError } from '@/lib/api/client';
import { 
  ArrowLeft, 
  ShieldAlert, 
  Dumbbell, 
  Target, 
  Info, 
  ExternalLink,
  CheckCircle2
} from 'lucide-react';

interface ExerciseDetail {
  id: string;
  slug: string;
  name: string;
  category: string;
  difficulty: string;
  primary_muscles: string[];
  secondary_muscles: string[];
  equipment_needed: string[];
  suitable_age_groups: string[];
  instructions: string;
  tips?: string;
  contraindications?: string;
  media: Array<{
    url: string;
    license_type: string;
    attribution_text: string;
  }>;
}

export default function ExerciseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params?.slug as string;

  const [exercise, setExercise] = React.useState<ExerciseDetail | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  React.useEffect(() => {
    async function fetchDetail() {
      if (!slug) return;
      setIsLoading(true);
      setErrorMsg(null);
      try {
        const res = await apiClient<ExerciseDetail>(`/exercises/${slug}`);
        setExercise(res);
      } catch (err: unknown) {
        if (err instanceof ApiError && err.code === 'NOT_FOUND') {
          setErrorMsg('Exercise not found in the catalog.');
        } else {
          const msg = err instanceof Error ? err.message : 'Failed to load exercise';
          setErrorMsg(msg);
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchDetail();
  }, [slug]);

  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-6 max-w-4xl mx-auto">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-72 w-full" />
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  if (errorMsg || !exercise) {
    return (
      <div className="p-6 md:p-10 max-w-xl mx-auto space-y-4">
        <Alert variant="error" title="Exercise Catalog">
          {errorMsg || 'Exercise not found.'}
        </Alert>
        <Link href="/exercises">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" /> Return to Exercise Library
          </Button>
        </Link>
      </div>
    );
  }

  const primaryMedia = exercise.media?.[0];

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-5xl mx-auto">
      
      {/* Back Link */}
      <Link href="/exercises" className="inline-flex items-center text-xs font-mono uppercase tracking-widest text-sand hover:text-lime transition-colors duration-fast">
        <ArrowLeft className="mr-2 h-3.5 w-3.5" /> Back to Exercise Library
      </Link>

      {/* Header & Badges */}
      <div className="space-y-3 border-b border-forest pb-6">
        <div className="flex flex-wrap gap-2">
          <Badge variant="lime">{exercise.category}</Badge>
          <Badge variant="forest">{exercise.difficulty}</Badge>
          {exercise.suitable_age_groups.map((ag) => (
            <Badge key={ag} variant="sand">
              {ag.replace('_', ' ')}
            </Badge>
          ))}
        </div>

        <h1 className="font-display text-3xl sm:text-5xl font-bold tracking-tight text-chalk uppercase">
          {exercise.name}
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Media & Biomechanical Details */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Demonstration Media Card */}
          <Card className="overflow-hidden border-forest">
            <div className="relative h-80 sm:h-96 w-full bg-forest/30">
              <Image
                src={primaryMedia?.url || 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80'}
                alt={exercise.name}
                fill
                priority
                sizes="(max-width: 1024px) 100vw, 60vw"
                className="object-cover"
              />
            </div>
            {primaryMedia && (
              <div className="p-3 bg-carbon border-t border-forest text-[11px] font-mono text-sand/80 flex items-center justify-between">
                <span>{primaryMedia.attribution_text}</span>
                <span className="text-lime">{primaryMedia.license_type}</span>
              </div>
            )}
          </Card>

          {/* Execution Instructions */}
          <Card>
            <CardHeader>
              <CardTitle>Biomechanical Execution</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-chalk leading-relaxed font-mono">
                {exercise.instructions}
              </p>
            </CardContent>
          </Card>

          {/* Coaching Cues */}
          {exercise.tips && (
            <Card className="border-forest/80 bg-forest/20">
              <CardHeader>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-lime" />
                  <CardTitle>Technique &amp; Form Cues</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-xs text-chalk leading-relaxed font-mono">
                  {exercise.tips}
                </p>
              </CardContent>
            </Card>
          )}

          {/* Clinical Contraindications */}
          {exercise.contraindications && (
            <Alert variant="warning" title="Clinical Contraindications">
              {exercise.contraindications}
            </Alert>
          )}

        </div>

        {/* Right Column: Anatomical Telemetry */}
        <div className="lg:col-span-5 space-y-6">
          
          <Card>
            <CardHeader>
              <CardTitle>Target Anatomy</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 font-mono text-xs">
              <div className="space-y-2">
                <span className="text-sand uppercase tracking-wider block">Primary Drivers</span>
                <div className="flex flex-wrap gap-1.5">
                  {exercise.primary_muscles.map((m) => (
                    <span
                      key={m}
                      className="px-2.5 py-1 bg-lime/10 border border-lime/40 text-lime font-semibold rounded-sm uppercase"
                    >
                      {m.replace('_', ' ')}
                    </span>
                  ))}
                </div>
              </div>

              {exercise.secondary_muscles.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-forest">
                  <span className="text-sand uppercase tracking-wider block">Synergists &amp; Stabilizers</span>
                  <div className="flex flex-wrap gap-1.5">
                    {exercise.secondary_muscles.map((m) => (
                      <span
                        key={m}
                        className="px-2 py-0.5 bg-forest/40 border border-forest text-sand rounded-sm uppercase"
                      >
                        {m.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Equipment Specification</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 font-mono text-xs">
              <div className="flex items-center gap-2 text-chalk">
                <Dumbbell className="h-4 w-4 text-lime" />
                <span className="uppercase">{exercise.equipment_needed.join(', ') || 'Bodyweight'}</span>
              </div>
            </CardContent>
          </Card>

        </div>

      </div>

    </div>
  );
}
