'use client';

import * as React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Alert } from '@/components/ui/alert';
import { createClient } from '@/lib/supabase/client';
import { Lock, Mail, User, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmPassword, setConfirmPassword] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);
  const [isVerificationSent, setIsVerificationSent] = React.useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password || !fullName) {
      setErrorMsg('Please complete all required fields.');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMsg('Passwords do not match.');
      return;
    }

    if (password.length < 8) {
      setErrorMsg('Password must be at least 8 characters long.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const supabase = createClient();
      const origin = window.location.origin;
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
          },
          emailRedirectTo: `${origin}/auth/callback`,
        },
      });

      if (error) {
        setErrorMsg(error.message);
        setIsLoading(false);
        return;
      }

      // If Supabase has email confirmation enabled
      if (data.user && !data.session) {
        setIsVerificationSent(true);
        setIsLoading(false);
        return;
      }

      // Immediate session
      router.push('/onboarding');
      router.refresh();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Registration failed';
      setErrorMsg(msg);
      setIsLoading(false);
    }
  };

  if (isVerificationSent) {
    return (
      <div className="min-h-screen flex flex-col justify-center items-center px-4 py-12 bg-carbon">
        <div className="w-full max-w-md">
          <Card className="border-lime/40">
            <CardHeader className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-sm bg-lime/10 text-lime mb-3">
                <CheckCircle2 className="h-6 w-6 text-lime" />
              </div>
              <CardTitle>Verification Email Sent</CardTitle>
              <CardDescription>
                We have dispatched a secure confirmation link to <span className="text-chalk font-semibold">{email}</span>.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-center">
              <p className="text-sm text-sand leading-relaxed">
                Please click the link in your email to verify your athlete profile and begin the onboarding assessment.
              </p>
              <Link href="/login">
                <Button variant="outline" className="w-full">
                  Return to Sign In
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-12 bg-carbon">
      <div className="w-full max-w-md space-y-6">
        
        <div className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <span className="h-3 w-3 bg-lime" />
            <span className="font-display text-2xl font-bold tracking-tighter text-chalk">
              FITGUIDE<span className="text-lime">.AI</span>
            </span>
          </Link>
          <p className="text-xs font-mono uppercase tracking-widest text-sand">
            NEW ATHLETE REGISTRATION
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Create Profile</CardTitle>
            <CardDescription>
              Register your account to receive personalized workouts and safety-guided programming.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            {errorMsg && (
              <Alert variant="error" title="Registration Error">
                {errorMsg}
              </Alert>
            )}

            <form onSubmit={handleRegister} className="space-y-3.5">
              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase tracking-wider text-sand flex items-center gap-1.5">
                  <User className="h-3.5 w-3.5 text-lime" /> Athlete Name
                </label>
                <Input
                  type="text"
                  placeholder="Jordan Vance"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  disabled={isLoading}
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase tracking-wider text-sand flex items-center gap-1.5">
                  <Mail className="h-3.5 w-3.5 text-lime" /> Email Address
                </label>
                <Input
                  type="email"
                  placeholder="athlete@domain.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase tracking-wider text-sand flex items-center gap-1.5">
                  <Lock className="h-3.5 w-3.5 text-lime" /> Password (Min. 8 characters)
                </label>
                <Input
                  type="password"
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLoading}
                  required
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-mono uppercase tracking-wider text-sand flex items-center gap-1.5">
                  <Lock className="h-3.5 w-3.5 text-lime" /> Confirm Password
                </label>
                <Input
                  type="password"
                  placeholder="••••••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={isLoading}
                  required
                />
              </div>

              <Button
                type="submit"
                variant="primary"
                className="w-full mt-2"
                isLoading={isLoading}
              >
                Create Account <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </form>
          </CardContent>

          <CardFooter className="justify-center border-t border-forest/40 pt-4">
            <p className="text-xs text-sand font-mono">
              Already have an account?{' '}
              <Link href="/login" className="text-lime hover:underline font-semibold ml-1">
                Sign in
              </Link>
            </p>
          </CardFooter>
        </Card>

      </div>
    </div>
  );
}
