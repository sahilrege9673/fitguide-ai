'use client';

import * as React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Alert } from '@/components/ui/alert';
import { createClient } from '@/lib/supabase/client';
import { Mail, ArrowLeft, CheckCircle2 } from 'lucide-react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [isSent, setIsSent] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setErrorMsg('Please enter your account email.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const supabase = createClient();
      const origin = window.location.origin;
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${origin}/auth/callback?next=/auth/reset-password`,
      });

      if (error) {
        setErrorMsg(error.message);
        setIsLoading(false);
        return;
      }

      setIsSent(true);
      setIsLoading(false);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Reset failed';
      setErrorMsg(msg);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-12 bg-carbon">
      <div className="w-full max-w-md space-y-6">
        
        <div className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <span className="h-3 w-3 bg-lime" />
            <span className="font-display text-2xl font-bold tracking-tighter text-chalk">
              FEEDGUIDE<span className="text-lime">.AI</span>
            </span>
          </Link>
          <p className="text-xs font-mono uppercase tracking-widest text-sand">
            CREDENTIAL RECOVERY
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Reset Password</CardTitle>
            <CardDescription>
              Enter your email address and we will dispatch a secure reset link.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            {errorMsg && (
              <Alert variant="error" title="Error">
                {errorMsg}
              </Alert>
            )}

            {isSent ? (
              <Alert variant="success" title="Recovery Link Sent">
                A password reset email has been dispatched to {email}. Check your inbox and spam folder.
              </Alert>
            ) : (
              <form onSubmit={handleReset} className="space-y-4">
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

                <Button
                  type="submit"
                  variant="primary"
                  className="w-full"
                  isLoading={isLoading}
                >
                  Send Recovery Link
                </Button>
              </form>
            )}
          </CardContent>

          <CardFooter className="justify-center border-t border-forest/40 pt-4">
            <Link href="/login" className="text-xs text-sand font-mono hover:text-chalk flex items-center gap-1">
              <ArrowLeft className="h-3.5 w-3.5" /> Back to Sign In
            </Link>
          </CardFooter>
        </Card>

      </div>
    </div>
  );
}
