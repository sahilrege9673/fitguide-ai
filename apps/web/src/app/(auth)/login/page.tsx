'use client';

import * as React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Alert } from '@/components/ui/alert';
import { createClient } from '@/lib/supabase/client';
import { Lock, Mail, ArrowRight } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const supabase = createClient();
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        setErrorMsg(error.message);
        setIsLoading(false);
        return;
      }

      router.push('/dashboard');
      router.refresh();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Authentication failed';
      setErrorMsg(msg);
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setIsGoogleLoading(true);
    setErrorMsg(null);
    try {
      const supabase = createClient();
      const origin = window.location.origin;
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${origin}/auth/callback`,
        },
      });
      if (error) {
        setErrorMsg(error.message);
        setIsGoogleLoading(false);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Google OAuth failed';
      setErrorMsg(msg);
      setIsGoogleLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-12 bg-carbon">
      <div className="w-full max-w-md space-y-6">
        
        {/* Brand Kicker */}
        <div className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <span className="h-3 w-3 bg-lime" />
            <span className="font-display text-2xl font-bold tracking-tighter text-chalk">
              FITGUIDE<span className="text-lime">.AI</span>
            </span>
          </Link>
          <p className="text-xs font-mono uppercase tracking-widest text-sand">
            ATHLETE AUTHENTICATION PORTAL
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Sign In</CardTitle>
            <CardDescription>
              Access your training schedule, exercise logs, and AI assistant.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            {errorMsg && (
              <Alert variant="error" title="Authentication Error">
                {errorMsg}
              </Alert>
            )}

            <form onSubmit={handleEmailLogin} className="space-y-4">
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
                <div className="flex items-center justify-between">
                  <label className="text-xs font-mono uppercase tracking-wider text-sand flex items-center gap-1.5">
                    <Lock className="h-3.5 w-3.5 text-lime" /> Password
                  </label>
                  <Link
                    href="/forgot-password"
                    className="text-xs font-mono text-sand hover:text-chalk underline underline-offset-2"
                  >
                    Forgot?
                  </Link>
                </div>
                <Input
                  type="password"
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
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
                Sign In <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </form>

            <div className="relative my-6 text-center">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-forest" />
              </div>
              <span className="relative bg-carbon-surface px-3 text-[10px] font-mono uppercase tracking-widest text-sand">
                Or Continue With
              </span>
            </div>

            <Button
              type="button"
              variant="outline"
              className="w-full font-mono text-xs"
              onClick={handleGoogleLogin}
              isLoading={isGoogleLoading}
            >
              Sign In with Google
            </Button>
          </CardContent>

          <CardFooter className="justify-center border-t border-forest/40 pt-4">
            <p className="text-xs text-sand font-mono">
              Don&apos;t have an athlete account?{' '}
              <Link href="/register" className="text-lime hover:underline font-semibold ml-1">
                Register here
              </Link>
            </p>
          </CardFooter>
        </Card>

      </div>
    </div>
  );
}
