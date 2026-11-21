'use client';

import * as React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { apiClient } from '@/lib/api/client';
import { createClient } from '@/lib/supabase/client';
import { 
  User, 
  Mail, 
  ShieldCheck, 
  Download, 
  Trash2, 
  Clock, 
  Dumbbell, 
  Edit3, 
  LogOut 
} from 'lucide-react';

interface ProfileData {
  id: string;
  email: string;
  full_name?: string;
  role: string;
  created_at: string;
}

interface PreferencesData {
  age_group: string;
  experience_level: string;
  fitness_goals: string[];
  workout_location: string;
  available_equipment: string[];
  time_availability_mins: number;
  preferred_days: number[];
}

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = React.useState<ProfileData | null>(null);
  const [preferences, setPreferences] = React.useState<PreferencesData | null>(null);
  const [fullNameInput, setFullNameInput] = React.useState('');
  const [isUpdating, setIsUpdating] = React.useState(false);
  const [isExporting, setIsExporting] = React.useState(false);
  const [isDeleting, setIsDeleting] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(true);
  const [alertMsg, setAlertMsg] = React.useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const loadProfile = React.useCallback(async () => {
    setIsLoading(true);
    setAlertMsg(null);
    try {
      const prof = await apiClient<ProfileData>('/profile');
      setProfile(prof);
      setFullNameInput(prof.full_name || '');

      const prefs = await apiClient<PreferencesData>('/onboarding').catch(() => null);
      setPreferences(prefs);
    } catch (err: unknown) {
      console.error('Failed to load profile:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  React.useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  const handleUpdateName = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsUpdating(true);
    setAlertMsg(null);
    try {
      const updated = await apiClient<ProfileData>('/profile', {
        method: 'PATCH',
        body: JSON.stringify({ full_name: fullNameInput }),
      });
      setProfile(updated);
      setAlertMsg({ type: 'success', text: 'Athlete profile updated successfully.' });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Update failed';
      setAlertMsg({ type: 'error', text: msg });
    } finally {
      setIsUpdating(false);
    }
  };

  const handleExportData = async () => {
    setIsExporting(true);
    try {
      const data = await apiClient<any>('/profile/export');
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `feedguide-telemetry-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export error:', err);
    } finally {
      setIsExporting(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmText !== profile?.email) return;

    setIsDeleting(true);
    try {
      await apiClient('/profile', { method: 'DELETE' });
      const supabase = createClient();
      await supabase.auth.signOut();
      router.push('/login');
      router.refresh();
    } catch (err) {
      console.error('Delete error:', err);
      setIsDeleting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-10 space-y-6 max-w-4xl mx-auto">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-48 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  return (
    <div className="p-6 md:p-10 space-y-8 max-w-5xl mx-auto">
      
      {/* Header */}
      <div className="border-b border-forest pb-6 space-y-1">
        <div className="flex items-center gap-2">
          <Badge variant="lime">ATHLETE IDENTITY</Badge>
          <span className="text-xs font-mono uppercase tracking-widest text-sand">
            ACCOUNT &amp; PREFERENCES
          </span>
        </div>
        <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight text-chalk uppercase">
          PROFILE &amp; SETTINGS
        </h1>
      </div>

      {alertMsg && (
        <Alert variant={alertMsg.type} title={alertMsg.type === 'success' ? 'Success' : 'Notice'}>
          {alertMsg.text}
        </Alert>
      )}

      {/* PERSONAL INFO CARD */}
      <Card>
        <CardHeader>
          <CardTitle>Personal Details</CardTitle>
          <CardDescription>
            Manage your display name and verified authentication identity.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpdateName} className="space-y-4 max-w-lg">
            <div className="space-y-1.5">
              <label className="text-xs font-mono uppercase text-sand flex items-center gap-1.5">
                <User className="h-3.5 w-3.5 text-lime" /> Full Name
              </label>
              <Input
                type="text"
                value={fullNameInput}
                onChange={(e) => setFullNameInput(e.target.value)}
                required
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-mono uppercase text-sand flex items-center gap-1.5">
                <Mail className="h-3.5 w-3.5 text-lime" /> Email Address (Verified)
              </label>
              <Input
                type="email"
                value={profile?.email || ''}
                disabled
                className="opacity-70 cursor-not-allowed"
              />
            </div>

            <Button type="submit" variant="primary" size="sm" isLoading={isUpdating}>
              Save Profile Changes
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* FITNESS PREFERENCES OVERVIEW */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Training Parameters</CardTitle>
            <CardDescription>
              Configured during onboarding to ground your weekly periodization.
            </CardDescription>
          </div>
          <Link href="/onboarding">
            <Button variant="outline" size="sm" className="font-mono text-xs">
              <Edit3 className="mr-1.5 h-3.5 w-3.5" /> Re-enter Onboarding
            </Button>
          </Link>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 font-mono text-xs">
            <div className="bg-carbon p-3.5 rounded-sm border border-forest space-y-1">
              <span className="text-sand uppercase">Physiology Group:</span>
              <p className="text-chalk font-semibold uppercase">{preferences?.age_group.replace('_', ' ')}</p>
            </div>
            <div className="bg-carbon p-3.5 rounded-sm border border-forest space-y-1">
              <span className="text-sand uppercase">Experience Level:</span>
              <p className="text-chalk font-semibold uppercase">{preferences?.experience_level}</p>
            </div>
            <div className="bg-carbon p-3.5 rounded-sm border border-forest space-y-1">
              <span className="text-sand uppercase">Session Duration:</span>
              <p className="text-lime font-semibold">{preferences?.time_availability_mins} Minutes</p>
            </div>
            <div className="bg-carbon p-3.5 rounded-sm border border-forest space-y-1 sm:col-span-2">
              <span className="text-sand uppercase">Available Gear:</span>
              <p className="text-chalk font-semibold">{preferences?.available_equipment.join(', ') || 'Bodyweight'}</p>
            </div>
            <div className="bg-carbon p-3.5 rounded-sm border border-forest space-y-1">
              <span className="text-sand uppercase">Weekly Days:</span>
              <p className="text-chalk font-semibold">{preferences?.preferred_days.length} Days Active</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* DATA PORTABILITY & PRIVACY (GDPR / CCPA) */}
      <Card>
        <CardHeader>
          <CardTitle>Data Portability &amp; Privacy</CardTitle>
          <CardDescription>
            Export all stored telemetry, workout logs, and profile records in standard JSON format.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-xs text-sand font-mono max-w-xl leading-relaxed">
            In compliance with international data privacy standards, you have the right to download a machine-readable copy of your entire physical training archive.
          </p>
          <Button variant="outline" size="sm" onClick={handleExportData} isLoading={isExporting}>
            <Download className="mr-2 h-4 w-4" /> Download Personal Data Bundle (.json)
          </Button>
        </CardContent>
      </Card>

      {/* DANGER ZONE (Account Deletion) */}
      <Card className="border-burnt/40 bg-burnt/5">
        <CardHeader>
          <CardTitle className="text-burnt">Danger Zone</CardTitle>
          <CardDescription>
            Irreversible actions that purge your athlete profile and training telemetry.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-xs text-sand font-mono max-w-xl leading-relaxed">
            Deleting your account immediately purges your profile, onboarding records, schedule entries, and historical workout logs. This action cannot be reversed.
          </p>
          <Button variant="danger" size="sm" onClick={() => setShowDeleteModal(true)}>
            <Trash2 className="mr-2 h-4 w-4" /> Delete Account &amp; All Data
          </Button>
        </CardContent>
      </Card>

      {/* DELETE CONFIRMATION MODAL */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-carbon/80 backdrop-blur-sm p-4">
          <Card className="w-full max-w-md border-burnt bg-carbon space-y-4 shadow-2xl">
            <CardHeader>
              <CardTitle className="text-burnt">Confirm Permanent Deletion</CardTitle>
              <CardDescription>
                To confirm deletion, please type your email address below: <br />
                <span className="font-mono text-chalk font-semibold">{profile?.email}</span>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 font-mono text-xs">
              <Input
                type="text"
                placeholder={profile?.email}
                value={deleteConfirmText}
                onChange={(e) => setDeleteConfirmText(e.target.value)}
              />
            </CardContent>
            <div className="p-6 pt-0 border-t border-forest/60 flex items-center justify-between">
              <Button variant="ghost" onClick={() => setShowDeleteModal(false)} disabled={isDeleting}>
                Cancel
              </Button>
              <Button
                variant="danger"
                onClick={handleDeleteAccount}
                disabled={deleteConfirmText !== profile?.email || isDeleting}
                isLoading={isDeleting}
              >
                Permanently Delete
              </Button>
            </div>
          </Card>
        </div>
      )}

    </div>
  );
}
