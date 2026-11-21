'use client';

import * as React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert } from '@/components/ui/alert';
import { apiClient } from '@/lib/api/client';
import { Search, Filter, Dumbbell, ArrowRight, ShieldCheck } from 'lucide-react';

interface ExerciseItem {
  id: string;
  slug: string;
  name: string;
  category: string;
  difficulty: string;
  primary_muscles: string[];
  equipment_needed: string[];
  suitable_age_groups: string[];
  instructions: string;
  media: Array<{
    url: string;
    attribution_text: string;
  }>;
}

interface ExerciseListResponse {
  data: ExerciseItem[];
  page: number;
  page_size: number;
  total_records: number;
  total_pages: number;
}

const MUSCLE_FILTERS = [
  { id: '', label: 'All Muscles' },
  { id: 'quadriceps', label: 'Quads' },
  { id: 'hamstrings', label: 'Hamstrings' },
  { id: 'glutes', label: 'Glutes' },
  { id: 'chest', label: 'Chest' },
  { id: 'lats', label: 'Lats & Back' },
  { id: 'deltoids', label: 'Shoulders' },
  { id: 'biceps', label: 'Biceps' },
  { id: 'triceps', label: 'Triceps' },
  { id: 'core', label: 'Core' },
];

export default function ExerciseLibraryPage() {
  const [exercises, setExercises] = React.useState<ExerciseItem[]>([]);
  const [totalCount, setTotalCount] = React.useState(0);
  const [search, setSearch] = React.useState('');
  const [selectedMuscle, setSelectedMuscle] = React.useState('');
  const [selectedCategory, setSelectedCategory] = React.useState('');
  const [selectedDifficulty, setSelectedDifficulty] = React.useState('');
  const [selectedEquipment, setSelectedEquipment] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(true);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const fetchExercises = React.useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const params = new URLSearchParams();
      if (search.trim()) params.append('search', search.trim());
      if (selectedMuscle) params.append('muscle', selectedMuscle);
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedDifficulty) params.append('difficulty', selectedDifficulty);
      if (selectedEquipment) params.append('equipment', selectedEquipment);
      params.append('page_size', '60');

      const res = await apiClient<ExerciseListResponse>(`/exercises?${params.toString()}`);
      setExercises(res.data);
      setTotalCount(res.total_records);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch exercise catalog';
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  }, [search, selectedMuscle, selectedCategory, selectedDifficulty, selectedEquipment]);

  React.useEffect(() => {
    const timer = setTimeout(() => {
      fetchExercises();
    }, 250);
    return () => clearTimeout(timer);
  }, [fetchExercises]);

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-7xl mx-auto">
      
      {/* Editorial Header */}
      <div className="border-b border-forest pb-6 space-y-2">
        <div className="flex items-center gap-2">
          <Badge variant="lime">VERIFIED CATALOG</Badge>
          <span className="text-xs font-mono uppercase tracking-widest text-sand">
            BIOMECHANICAL REFERENCE DATABASE
          </span>
        </div>
        <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight text-chalk uppercase">
          EXERCISE LIBRARY
        </h1>
        <p className="text-sm text-sand leading-relaxed max-w-2xl font-mono">
          Authoritative database of {totalCount || '84'} movements with biomechanical instructions, 
          equipment compatibility, and licensed demonstration photography.
        </p>
      </div>

      {/* FILTER CONTROLS */}
      <div className="space-y-4">
        
        {/* Search Bar & Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
          <div className="sm:col-span-6 relative">
            <Search className="absolute left-3.5 top-3.5 h-4 w-4 text-sand" />
            <Input
              type="text"
              placeholder="Search exercise name or instructions..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>

          <div className="sm:col-span-3">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="h-11 w-full rounded-sm border border-forest bg-carbon-surface px-3 text-xs font-mono text-chalk focus:outline-none focus:ring-2 focus:ring-lime"
            >
              <option value="">All Categories</option>
              <option value="strength">Strength</option>
              <option value="hypertrophy">Hypertrophy</option>
              <option value="conditioning">Conditioning</option>
              <option value="mobility">Mobility</option>
            </select>
          </div>

          <div className="sm:col-span-3">
            <select
              value={selectedEquipment}
              onChange={(e) => setSelectedEquipment(e.target.value)}
              className="h-11 w-full rounded-sm border border-forest bg-carbon-surface px-3 text-xs font-mono text-chalk focus:outline-none focus:ring-2 focus:ring-lime"
            >
              <option value="">All Equipment</option>
              <option value="barbell">Barbell</option>
              <option value="dumbbells">Dumbbells</option>
              <option value="cable_machine">Cable Machine</option>
              <option value="pull_up_bar">Pull-Up Bar</option>
              <option value="kettlebells">Kettlebells</option>
              <option value="bodyweight">Bodyweight Only</option>
            </select>
          </div>
        </div>

        {/* Muscle Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-none">
          {MUSCLE_FILTERS.map((mf) => (
            <button
              key={mf.id}
              onClick={() => setSelectedMuscle(mf.id)}
              className={`px-3 py-1.5 rounded-sm text-xs font-mono uppercase tracking-wider shrink-0 transition-colors duration-fast ${
                selectedMuscle === mf.id
                  ? 'bg-lime text-carbon font-semibold'
                  : 'bg-forest/40 text-sand hover:text-chalk border border-forest'
              }`}
            >
              {mf.label}
            </button>
          ))}
        </div>

      </div>

      {errorMsg && (
        <Alert variant="error" title="Query Error">
          {errorMsg}
        </Alert>
      )}

      {/* EXERCISE CARDS GRID */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="h-48 w-full" />
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </div>
          ))}
        </div>
      ) : exercises.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {exercises.map((ex) => {
            const mediaUrl = ex.media?.[0]?.url || 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80';
            return (
              <Link key={ex.id} href={`/exercises/${ex.slug}`} className="group">
                <Card className="h-full overflow-hidden border-forest hover:border-lime/60 transition-colors duration-fast flex flex-col justify-between">
                  <div>
                    {/* Media Image */}
                    <div className="relative h-48 w-full bg-forest/30 overflow-hidden">
                      <Image
                        src={mediaUrl}
                        alt={ex.name}
                        fill
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        className="object-cover group-hover:scale-105 transition-transform duration-normal"
                        loading="lazy"
                      />
                      <div className="absolute top-2.5 left-2.5 flex gap-1.5">
                        <Badge variant="lime">{ex.category}</Badge>
                        <Badge variant="forest">{ex.difficulty}</Badge>
                      </div>
                    </div>

                    <div className="p-5 space-y-3">
                      <h3 className="font-display text-lg font-bold text-chalk group-hover:text-lime transition-colors duration-fast uppercase tracking-tight">
                        {ex.name}
                      </h3>

                      <p className="text-xs text-sand/80 line-clamp-2 leading-relaxed font-mono">
                        {ex.instructions}
                      </p>

                      <div className="flex flex-wrap gap-1.5 pt-1">
                        {ex.primary_muscles.map((m) => (
                          <span
                            key={m}
                            className="text-[10px] font-mono text-sand bg-forest/40 border border-forest px-1.5 py-0.5 rounded-sm"
                          >
                            {m.replace('_', ' ')}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="px-5 py-3 border-t border-forest/50 bg-carbon flex items-center justify-between text-xs font-mono text-sand group-hover:text-chalk">
                    <span>{ex.equipment_needed.join(', ') || 'Bodyweight'}</span>
                    <ArrowRight className="h-4 w-4 text-lime group-hover:translate-x-1 transition-transform duration-fast" />
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      ) : (
        /* EMPTY STATE */
        <Card className="p-12 text-center border-forest/60 bg-carbon-surface space-y-4">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-sm bg-forest/30 text-sand">
            <Dumbbell className="h-7 w-7" />
          </div>
          <div className="space-y-1">
            <h3 className="font-display text-lg font-bold text-chalk uppercase">
              No Matching Exercises Found
            </h3>
            <p className="text-xs text-sand font-mono max-w-md mx-auto">
              No exercise matches your current search query and filters. Try clearing some filter selections.
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSearch('');
              setSelectedMuscle('');
              setSelectedCategory('');
              setSelectedDifficulty('');
              setSelectedEquipment('');
            }}
          >
            Reset Filters
          </Button>
        </Card>
      )}

    </div>
  );
}
