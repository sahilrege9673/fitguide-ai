import type { Metadata } from 'next';
import './globals.css';

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
      <body className="min-h-screen bg-carbon text-chalk antialiased selection:bg-lime selection:text-carbon font-body">
        {children}
      </body>
    </html>
  );
}
