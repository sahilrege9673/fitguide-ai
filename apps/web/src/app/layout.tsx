import type { Metadata } from 'next';
import './globals.css';
import { ServerWarmup } from '@/components/layout/server-warmup';

export const metadata: Metadata = {
  title: 'FitGuide AI — Engineered Fitness Companion',
  description: 'Grounded fitness planning, structured periodization, and clinical safety guardrails.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fitguide-ai.onrender.com" />
        <link rel="dns-prefetch" href="https://fitguide-ai.onrender.com" />
      </head>
      <body className="min-h-screen bg-carbon text-chalk antialiased selection:bg-lime selection:text-carbon font-body">
        <ServerWarmup />
        {children}
      </body>
    </html>
  );
}
